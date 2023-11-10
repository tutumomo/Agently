from .utils import PluginManager, StorageDelegate
from .plugins import install_plugins
from .WebSocket import WebSocketServer

global_plugin_manager = PluginManager()
install_plugins(global_plugin_manager)
global_storage = StorageDelegate(
    db_name = "global",
    plugin_manager = global_plugin_manager,
)
global_websocket_server = WebSocketServer()