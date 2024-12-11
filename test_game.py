import pytest
from models.game import Game
from models.players import Player
import os
import json
from unittest.mock import patch


# --- Player Class Tests ---

def test_player_initialization():
    player = Player("TestPlayer")
    assert player.pseudo == "TestPlayer"
    assert player.current_vote is None
    assert "5" in player.cards

def test_player_vote_valid():
    player = Player("TestPlayer")
    player.vote("5")
    assert player.current_vote == "5"

def test_player_vote_invalid():
    player = Player("TestPlayer")
    with pytest.raises(ValueError, match="Invalid card: 50"):
        player.vote("50")

def test_player_reset_vote():
    player = Player("TestPlayer")
    player.vote("8")
    player.reset_vote()
    assert player.current_vote is None


# --- Game Class Tests ---

def test_game_initialization():
    with patch("builtins.input", side_effect=["Player1", "Player2"]):
        game = Game(num_players=2, rules="strict")
        assert game.rules == "strict"
        assert len(game.players) == 2

def test_backlog_loading(tmpdir):
    backlog_file = tmpdir.join("backlog.json")
    backlog_data = {"tasks": [{"description": "Test feature"}]}
    backlog_file.write(json.dumps(backlog_data))

    game = Game(num_players=0)
    game.load_backlog(str(backlog_file))
    assert len(game.backlog) == 1
    assert game.backlog[0]["description"] == "Test feature"

def test_game_state_saving_and_loading(tmpdir):
    save_file = tmpdir.join("game_state.json")
    with patch("builtins.input", side_effect=["Player1", "Player2"]):
        game = Game(num_players=2)
        game.save_game_state(str(save_file))
        assert os.path.exists(save_file)

        game.load_game_state(str(save_file))
        assert len(game.players) == 2

def test_process_votes_unanimity():
    with patch("builtins.input", side_effect=["Player1", "Player2", "Player3"]):
        game = Game(num_players=3, rules="strict")
        game.current_feature = {"description": "Test feature"}  # Mock feature
        for player in game.players:
            player.vote("5")
        assert game.process_votes() is True

def test_process_votes_no_unanimity():
    with patch("builtins.input", side_effect=["Player1", "Player2", "Player3"]):
        game = Game(num_players=3, rules="strict")
        game.players[0].vote("5")
        game.players[1].vote("8")
        game.players[2].vote("5")
        assert game.process_votes() is False