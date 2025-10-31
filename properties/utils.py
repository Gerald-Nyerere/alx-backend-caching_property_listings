from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

def get_all_properties():
    properties = cache.get('all_properties')

    if properties is None:
        print("Cache miss: Fetching from database...")
        properties = list(
            Property.objects.all().values(
                'id', 'title', 'description', 'price', 'location', 'created_at'
            )
        )
        cache.set('all_properties', properties, 3600)
    else:
        logger.info("Cache hit: Data retrieved from Redis.")

    return properties

def get_redis_cache_metrics():
    """
    Retrieve Redis cache statistics: hits, misses, and hit ratio.
    Returns a dictionary with keyspace_hits, keyspace_misses, and hit_ratio.
    """
    try:
        # Access the Redis client via django-redis
        client = cache.client.get_client(write=False)
        info = client.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else 0

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 4),
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis metrics: {e}")
        return {"error": str(e)}
