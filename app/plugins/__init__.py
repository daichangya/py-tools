from flask import Flask

def register_plugins(app: Flask):
    """注册所有插件蓝图"""
    from . import (
        bank_plugin, 
        express_plugin, 
        identity_plugin, 
        ip_plugin, 
        region_plugin, 
        quote_plugin,
        greeting_card_plugin,
        id_card_maker_plugin
    )

    app.register_blueprint(bank_plugin.bank_bp)
    app.register_blueprint(express_plugin.express_bp)
    app.register_blueprint(identity_plugin.identity_bp)
    app.register_blueprint(ip_plugin.ip_bp)
    app.register_blueprint(region_plugin.region_bp)
    app.register_blueprint(quote_plugin.quote_bp)
    app.register_blueprint(greeting_card_plugin.greeting_card_bp)
    app.register_blueprint(id_card_maker_plugin.id_card_maker_bp)