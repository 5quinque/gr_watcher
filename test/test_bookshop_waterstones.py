
import pytest

from gr_watcher.bookshops.Waterstones import Waterstones

def test_default_initial_values():
    waterstones = Waterstones("Nicholson Baker", "The Mezzanine")

    assert waterstones.author == "Nicholson Baker"
    assert waterstones.title == "The Mezzanine"

def test_get_price():
    waterstones = Waterstones("Nicholson Baker", "The Mezzanine")

    waterstones.get_price()

    assert type(waterstones.price) is float
    assert waterstones.price > 0.00

