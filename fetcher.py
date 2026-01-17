"""Enhanced HTTP fetcher with error handling, retries, and logging."""
import logging
import time
from typing import Optional
import requests
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DataScraper/1.0)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def fetch_html(url: str, retries: int = 3, timeout: int = 10, backoff_factor: float = 0.3) -> Optional[str]:
    """
    Fetch HTML content from a URL with retry logic and exponential backoff.
    
    Args:
        url: Target URL to scrape
        retries: Number of retry attempts (default: 3)
        timeout: Request timeout in seconds (default: 10)
        backoff_factor: Exponential backoff multiplier (default: 0.3)
        
    Returns:
        HTML content as string, or None if all attempts fail
        
    Example:
        >>> html = fetch_html("https://example.com")
        >>> if html:
        ...     print(f"Fetched {len(html)} characters")
    """
    for attempt in range(retries):
        try:
            logger.info(f"Fetching {url} (attempt {attempt + 1}/{retries})")
            
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=timeout,
                verify=True,
                allow_redirects=True
            )
            
            # Raise exception for bad status codes
            response.raise_for_status()
            
            logger.info(f"Successfully fetched {url} ({response.status_code})")
            return response.text
            
        except Timeout:
            logger.warning(f"Timeout on attempt {attempt + 1} for {url}")
            if attempt < retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                logger.info(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                logger.error(f"Failed to fetch {url} after {retries} attempts (Timeout)")
                return None
                
        except HTTPError as e:
            logger.error(f"HTTP error for {url}: {e.response.status_code} - {e}")
            # Don't retry on client errors (4xx)
            if 400 <= e.response.status_code < 500:
                return None
            # Retry on server errors (5xx)
            if attempt < retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                time.sleep(sleep_time)
            else:
                return None
                
        except ConnectionError:
            logger.warning(f"Connection error on attempt {attempt + 1} for {url}")
            if attempt < retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                time.sleep(sleep_time)
            else:
                logger.error(f"Failed to connect to {url} after {retries} attempts")
                return None
                
        except RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            return None
            
    return None


def fetch_html_with_session(
    session: requests.Session,
    url: str,
    retries: int = 3,
    timeout: int = 10
) -> Optional[str]:
    """
    Fetch HTML using a persistent session for connection pooling.
    
    Args:
        session: Requests session object
        url: Target URL to scrape
        retries: Number of retry attempts
        timeout: Request timeout in seconds
        
    Returns:
        HTML content as string, or None if failed
        
    Example:
        >>> with requests.Session() as session:
        ...     html = fetch_html_with_session(session, "https://example.com")
    """
    session.headers.update(HEADERS)
    
    for attempt in range(retries):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                return None
            time.sleep(0.3 * (2 ** attempt))
    
    return None
