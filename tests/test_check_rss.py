import pytest
from unittest.mock import patch, MagicMock
from utils import check_rss, last_articles

@pytest.fixture
def mock_feedparser():
    with patch('utils.check_rss.feedparser') as mock:
        yield mock

@pytest.fixture
def mock_beautifulsoup():
    with patch('utils.check_rss.BeautifulSoup') as mock:
        yield mock

@pytest.fixture(autouse=True)
def clear_last_articles():
    """Fixture pour réinitialiser last_articles avant chaque test"""
    last_articles.clear()

def test_check_rss_successful(mock_feedparser, mock_beautifulsoup):
    """Test d'un ajout d'article réussi"""
    # Configurer le mock pour feedparser
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [
        MagicMock(
            id='test_id_1', 
            title='Test Article', 
            link='http://test.com', 
            summary='Test summary', 
            dc_content='<p>Test content</p>'
        )
    ]
    mock_feedparser.parse.return_value = mock_feed

    # Configurer le mock pour BeautifulSoup
    mock_soup = MagicMock()
    mock_soup.get_text.return_value = 'Test content'
    mock_beautifulsoup.return_value = mock_soup

    check_rss()

    assert len(last_articles) == 1
    assert 'test_id_1' in last_articles
    assert last_articles['test_id_1'].title == 'Test Article'
    assert last_articles['test_id_1'].link == 'http://test.com'
    assert last_articles['test_id_1'].summary == 'Test summary'
    assert last_articles['test_id_1'].text == 'Test content'

def test_check_rss_limit_articles(mock_feedparser, mock_beautifulsoup):
    """Test de la limitation du nombre d'articles"""
    # Configurer le mock pour feedparser avec plus de 10 articles
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [
        MagicMock(
            id=f'id_{i}', 
            title=f'Test Article {i}', 
            link=f'http://test{i}.com', 
            summary=f'Test summary {i}', 
            dc_content=f'<p>Test content {i}</p>'
        )
        for i in range(14, -1, -1)
    ]
    mock_feedparser.parse.return_value = mock_feed

    # Configurer le mock pour BeautifulSoup
    mock_soup = MagicMock()
    mock_soup.get_text.return_value = 'Test content'
    mock_beautifulsoup.return_value = mock_soup

    check_rss()

    assert len(last_articles) == 10, "Le nombre d'articles devrait être limité à 10"
    print(last_articles)
    
    # Vérifier que les 10 derniers articles sont présents
    last_10_ids = [f'id_{i}' for i in range(5, 15)]
    for article_id in last_10_ids:
        assert article_id in last_articles, f"L'article {article_id} devrait être présent"

    # Vérifier que les 5 premiers articles ne sont pas présents
    first_5_ids = [f'id_{i}' for i in range(5)]
    for article_id in first_5_ids:
        assert article_id not in last_articles, f"L'article {article_id} ne devrait pas être présent"

def test_check_rss_bozo_error(mock_feedparser):
    """Test du comportement en cas d'erreur bozo"""
    # Configurer le mock pour simuler une erreur bozo
    mock_feed = MagicMock()
    mock_feed.bozo = True
    mock_feed.bozo_exception = "Test exception"
    mock_feedparser.parse.return_value = mock_feed

    check_rss()

    assert len(last_articles) == 0, "Aucun article ne devrait être ajouté en cas d'erreur"

def test_check_rss_attribute_error(mock_feedparser):
    """Test du comportement en cas d'AttributeError"""
    # Configurer le mock pour lever une AttributeError
    mock_feedparser.parse.side_effect = AttributeError("Test AttributeError")

    check_rss()

    assert len(last_articles) == 0, "Aucun article ne devrait être ajouté en cas d'erreur"

def test_check_rss_key_error(mock_feedparser):
    """Test du comportement en cas de KeyError"""
    # Configurer le mock pour lever une KeyError
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [MagicMock(spec=[])]  # Ceci causera une KeyError lors de l'accès aux attributs
    mock_feedparser.parse.return_value = mock_feed

    check_rss()

    assert len(last_articles) == 0, "Aucun article ne devrait être ajouté en cas d'erreur"