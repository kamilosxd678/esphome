import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_MODEL, CONF_CHARACTERISTIC_UUID, CONF_VALUE
from esphome.components import esp32_ble
from esphome.core import CORE
from esphome.components.esp32 import add_idf_sdkconfig_option

AUTO_LOAD = ["esp32_ble"]
CODEOWNERS = ["@jesserockz"]
CONFLICTS_WITH = ["esp32_ble_beacon"]
DEPENDENCIES = ["esp32"]

CONF_MANUFACTURER = "manufacturer"

esp32_ble_server_ns = cg.esphome_ns.namespace("esp32_ble_server")
BLEServer = esp32_ble_server_ns.class_(
    "BLEServer",
    cg.Component,
    esp32_ble.GATTsEventHandler,
    cg.Parented.template(esp32_ble.ESP32BLE),
)
BLEServiceComponent = esp32_ble_server_ns.class_("BLEServiceComponent")

BLE_PROPERITES = {
    "PROPERTY_READ": 1,
    "PROPERTY_WRITE": 2,
    "PROPERTY_NOTIFY": 4,
    "PROPERTY_BROADCAST": 8,
    "PROPERTY_INDICATE": 16,
    "PROPERTY_WRITE_NR": 32
}

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(BLEServer),
        cv.GenerateID(esp32_ble.CONF_BLE_ID): cv.use_id(esp32_ble.ESP32BLE),
        cv.Optional(CONF_MANUFACTURER, default="ESPHome"): cv.string,
        cv.Optional(CONF_MODEL): cv.string,
        cv.Optional("custom_characteristics"): cv.templatable(cv.ensure_list({
            #cv.GenerateID(CONF_ID): cv.use_id(BLEClient),
            cv.Required(CONF_CHARACTERISTIC_UUID): cv.string, #esp32_ble_tracker.bt_uuid,
            cv.Required("properties"): cv.templatable(cv.ensure_list(cv.one_of(*BLE_PROPERITES, upper=True))),
            cv.Required(CONF_VALUE): cv.templatable(cv.ensure_list(cv.hex_uint8_t)),
        }))
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])

    await cg.register_component(var, config)

    parent = await cg.get_variable(config[esp32_ble.CONF_BLE_ID])
    cg.add(parent.register_gatts_event_handler(var))
    cg.add(var.set_parent(parent))

    cg.add(var.set_manufacturer(config[CONF_MANUFACTURER]))
    if CONF_MODEL in config:
        cg.add(var.set_model(config[CONF_MODEL]))
    cg.add_define("USE_ESP32_BLE_SERVER")

    if "custom_characteristics" in config:
        print(config["custom_characteristics"])
        for x in config["custom_characteristics"]:
            ble_props = []
            props_ns = cg.esphome_ns.namespace("esp32_ble_server").namespace("BLECharacteristic")

            for prop in x["properties"]:
                ble_props.append(props_ns.prop)
                
            cg.add(var.add_custom_characteristics(x["characteristic_uuid"], ble_props))

    if CORE.using_esp_idf:
        add_idf_sdkconfig_option("CONFIG_BT_ENABLED", True)
