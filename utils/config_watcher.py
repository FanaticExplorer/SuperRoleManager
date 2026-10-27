import os

from discord.ext import tasks

from services.role_service import role_service
from utils.logger import logger

# Consecutive failures tolerated before waiting for the file to change again.
MAX_CONSECUTIVE_RELOAD_FAILURES = 3


class ConfigWatcher:
    """
    Monitors the config file for changes and automatically reloads it.
    Uses discord.ext.tasks.loop for efficient background monitoring.
    """

    def __init__(self, config_path: str = "config/roles.yaml"):
        self.config_path = config_path
        self.last_mtime = None
        self._reload_failures = 0

    @staticmethod
    def _get_file_mtime(file_path: str) -> float | None:
        """Get the modification time of the config file."""
        try:
            return os.path.getmtime(file_path)
        except OSError as e:
            logger.warning(f"Failed to get modification time for {file_path}: {e}")
            return None

    def _check_and_reload(self):
        """Check if file has changed and reload if needed."""
        current_mtime = self._get_file_mtime(self.config_path)

        if current_mtime is None:
            return

        # First run - just store the mtime
        if self.last_mtime is None:
            self.last_mtime = current_mtime
            logger.debug(f"Config watcher initialized. Current mtime: {current_mtime}")
            return

        # File has been modified
        if current_mtime != self.last_mtime:
            logger.debug(f"Config change detected! Old mtime: {self.last_mtime}, New mtime: {current_mtime}")
            old_count = len(role_service.categories)

            try:
                role_service.reload_config()
            # Malformed YAML shapes surface from the parser as these.
            except (AttributeError, TypeError) as e:
                self._reload_failures += 1
                if self._reload_failures < MAX_CONSECUTIVE_RELOAD_FAILURES:
                    # last_mtime stays untouched so the next tick retries.
                    logger.exception(
                        f"Failed to reload config, retrying "
                        f"({self._reload_failures}/{MAX_CONSECUTIVE_RELOAD_FAILURES}): {e}"
                    )
                    return

                # Give up until the file changes, otherwise a broken config would
                # log every tick forever.
                logger.exception(f"Failed to reload config, giving up for now: {e}")
                self.last_mtime = current_mtime
                self._reload_failures = 0
                return

            self.last_mtime = current_mtime
            self._reload_failures = 0
            new_count = len(role_service.categories)
            logger.info(
                f"🔄 Config reloaded: {new_count} categories loaded "
                f"(was {old_count})"
            )
            logger.debug(f"New categories: {[c.id for c in role_service.categories]}")

    def start(self):
        """Start the config watcher task."""
        if self._watch_config_loop.is_running():
            logger.warning("Config watcher is already running")
            return

        # Initialize mtime on first start
        self.last_mtime = self._get_file_mtime(self.config_path)

        self._watch_config_loop.start()
        logger.debug("Config watcher started (checking every 2 seconds)")

    def stop(self):
        """Stop the config watcher task."""
        if self._watch_config_loop.is_running():
            self._watch_config_loop.cancel()
            logger.debug("Config watcher stopped")

    @tasks.loop(seconds=2)
    async def _watch_config_loop(self):
        """Background task that checks for config changes every 2 seconds."""
        self._check_and_reload()

    @_watch_config_loop.before_loop
    async def before_watch_loop(self):
        """Wait for the bot to be ready before starting the loop."""
        # This decorator is kept for potential future bot integration


# Global instance
config_watcher = ConfigWatcher()
