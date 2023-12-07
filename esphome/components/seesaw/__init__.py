import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c
from esphome.const import CONF_FREQUENCY, CONF_ID, CONF_EXTERNAL_CLOCK_INPUT

DEPENDENCIES = ["i2c"]
MULTI_CONF = True

seesaw_ns = cg.esphome_ns.namespace("seesaw")
SeeSawOutput = seesaw_ns.class_("SeeSawOutput", cg.Component, i2c.I2CDevice)


CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(SeeSawOutput),
            cv.Optional(CONF_EXTERNAL_CLOCK_INPUT, default=False): cv.boolean,
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(i2c.i2c_device_schema(0x49))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)
    cg.add_library("adafruit/Adafruit BusIO", "1.14.5")
    cg.add_library("adafruit/Adafruit seesaw Library", "1.7.5")
