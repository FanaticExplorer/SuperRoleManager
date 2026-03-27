import os
from discord.ext import tasks
from utils.logger import logger
from services.role_service import role_service


class ConfigWatcher:
    """
    Monitors the config file for changes and automatically reloads it.
    Uses discord.ext.tasks.loop for efficient background monitoring.
    """

    def __init__(self, config_path: str = "config/roles.yaml"):
        self.config_path = config_path
        self.last_mtime = None
        self._watcher_task = None

    @staticmethod
    def _get_file_mtime(file_path: str) -> float | None:
        """Get the modification time of the config file."""
        try:
            return os.path.getmtime(file_path)
        except OSError as e:
            logger.error(f"Failed to get modification time for {file_path}: {e}")
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
            self.last_mtime = current_mtime
            old_count = len(role_service.categories)

            try:
                role_service.reload_config()
                new_count = len(role_service.categories)
                logger.info(
                    f"🔄 Config reloaded: {new_count} categories loaded "
                    f"(was {old_count})"
                )
                logger.debug(f"New categories: {[c.id for c in role_service.categories]}")
            except Exception as e:
                logger.error(f"Failed to reload config: {e}")
                # Restore old mtime on error to retry next time
                self.last_mtime = self._get_file_mtime(self.config_path)

    def start(self):
        """Start the config watcher task."""
        if self._watcher_task and self._watcher_task.is_running():
            logger.warning("Config watcher is already running")
            return

        # Initialize mtime on first start
        self.last_mtime = self._get_file_mtime(self.config_path)

        # Create and start the watcher task
        self._watcher_task = self._watch_config_loop.start()
        logger.info("Config watcher started (checking every 2 seconds)")

    def stop(self):
        """Stop the config watcher task."""
        if self._watcher_task and self._watcher_task.is_running():
            self._watcher_task.cancel()
            logger.info("Config watcher stopped")

    @tasks.loop(seconds=2)
    async def _watch_config_loop(self):
        """Background task that checks for config changes every 2 seconds."""
        self._check_and_reload()

    @_watch_config_loop.before_loop
    async def before_watch_loop(self):
        """Wait for the bot to be ready before starting the loop."""
        # This decorator is kept for potential future bot integration
        pass


# Global instance
config_watcher = ConfigWatcher()

