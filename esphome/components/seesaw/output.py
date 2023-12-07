import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import output
from esphome.const import CONF_CHANNEL, CONF_ID
from . import SeeSawOutput, seesaw_ns

DEPENDENCIES = ["seesaw"]

SeeSawChannel = seesaw_ns.class_("SeeSawChannel", output.FloatOutput)
CONF_SEESAW_ID = "seesaw_id"

CONFIG_SCHEMA = output.FLOAT_OUTPUT_SCHEMA.extend(
    {
        cv.Required(CONF_ID): cv.declare_id(SeeSawChannel),
        cv.GenerateID(CONF_SEESAW_ID): cv.use_id(SeeSawOutput),
        cv.Required(CONF_CHANNEL): cv.int_range(min=0, max=15),
    }
)


async def to_code(config):
    paren = await cg.get_variable(config[CONF_SEESAW_ID])
    var = cg.new_Pvariable(config[CONF_ID])
    cg.add(var.set_channel(config[CONF_CHANNEL]))
    cg.add(paren.register_channel(var))
    await output.register_output(var, config)
