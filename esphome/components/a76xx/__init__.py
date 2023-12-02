import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.const import (
    CONF_ID,
    CONF_TRIGGER_ID,
)
from esphome.components import uart

DEPENDENCIES = ["uart"]
CODEOWNERS = ["@glmnet"]
MULTI_CONF = True

a76xx_ns = cg.esphome_ns.namespace("a76xx")
A76XXComponent = a76xx_ns.class_("A76XXComponent", cg.Component)

A76XXReceivedMessageTrigger = a76xx_ns.class_(
    "A76XXReceivedMessageTrigger",
    automation.Trigger.template(cg.std_string, cg.std_string),
)
A76XXIncomingCallTrigger = a76xx_ns.class_(
    "A76XXIncomingCallTrigger",
    automation.Trigger.template(cg.std_string),
)
A76XXCallConnectedTrigger = a76xx_ns.class_(
    "A76XXCallConnectedTrigger",
    automation.Trigger.template(),
)
A76XXCallDisconnectedTrigger = a76xx_ns.class_(
    "A76XXCallDisconnectedTrigger",
    automation.Trigger.template(),
)

A76XXReceivedUssdTrigger = a76xx_ns.class_(
    "A76XXReceivedUssdTrigger",
    automation.Trigger.template(cg.std_string),
)

# Actions
A76XXSendSmsAction = a76xx_ns.class_("A76XXSendSmsAction", automation.Action)
A76XXSendUssdAction = a76xx_ns.class_("A76XXSendUssdAction", automation.Action)
A76XXDialAction = a76xx_ns.class_("A76XXDialAction", automation.Action)
A76XXConnectAction = a76xx_ns.class_("A76XXConnectAction", automation.Action)
A76XXDisconnectAction = a76xx_ns.class_(
    "A76XXDisconnectAction", automation.Action
)

CONF_A76XX_ID = "a76xx_id"
CONF_ON_SMS_RECEIVED = "on_sms_received"
CONF_ON_USSD_RECEIVED = "on_ussd_received"
CONF_ON_INCOMING_CALL = "on_incoming_call"
CONF_ON_CALL_CONNECTED = "on_call_connected"
CONF_ON_CALL_DISCONNECTED = "on_call_disconnected"
CONF_RECIPIENT = "recipient"
CONF_MESSAGE = "message"
CONF_USSD = "ussd"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(A76XXComponent),
            cv.Optional(CONF_ON_SMS_RECEIVED): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        A76XXReceivedMessageTrigger
                    ),
                }
            ),
            cv.Optional(CONF_ON_INCOMING_CALL): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        A76XXIncomingCallTrigger
                    ),
                }
            ),
            cv.Optional(CONF_ON_CALL_CONNECTED): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        A76XXCallConnectedTrigger
                    ),
                }
            ),
            cv.Optional(CONF_ON_CALL_DISCONNECTED): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        A76XXCallDisconnectedTrigger
                    ),
                }
            ),
            cv.Optional(CONF_ON_USSD_RECEIVED): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        A76XXReceivedUssdTrigger
                    ),
                }
            ),
        }
    )
    .extend(cv.polling_component_schema("5s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)
FINAL_VALIDATE_SCHEMA = uart.final_validate_device_schema(
    "a76xx", require_tx=True, require_rx=True
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    for conf in config.get(CONF_ON_SMS_RECEIVED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(
            trigger, [(cg.std_string, "message"), (cg.std_string, "sender")], conf
        )
    for conf in config.get(CONF_ON_INCOMING_CALL, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [(cg.std_string, "caller_id")], conf)
    for conf in config.get(CONF_ON_CALL_CONNECTED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], conf)
    for conf in config.get(CONF_ON_CALL_DISCONNECTED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], conf)

    for conf in config.get(CONF_ON_USSD_RECEIVED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [(cg.std_string, "ussd")], conf)


A76XX_SEND_SMS_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(A76XXComponent),
        cv.Required(CONF_RECIPIENT): cv.templatable(cv.string_strict),
        cv.Required(CONF_MESSAGE): cv.templatable(cv.string),
    }
)


@automation.register_action(
    "a76xx.send_sms", A76XXSendSmsAction, A76XX_SEND_SMS_SCHEMA
)
async def a76xx_send_sms_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_RECIPIENT], args, cg.std_string)
    cg.add(var.set_recipient(template_))
    template_ = await cg.templatable(config[CONF_MESSAGE], args, cg.std_string)
    cg.add(var.set_message(template_))
    return var


A76XX_DIAL_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(A76XXComponent),
        cv.Required(CONF_RECIPIENT): cv.templatable(cv.string_strict),
    }
)


@automation.register_action("a76xx.dial", A76XXDialAction, A76XX_DIAL_SCHEMA)
async def a76xx_dial_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_RECIPIENT], args, cg.std_string)
    cg.add(var.set_recipient(template_))
    return var


@automation.register_action(
    "a76xx.connect",
    A76XXConnectAction,
    cv.Schema({cv.GenerateID(): cv.use_id(A76XXComponent)}),
)
async def a76xx_connect_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    return var


A76XX_SEND_USSD_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(A76XXComponent),
        cv.Required(CONF_USSD): cv.templatable(cv.string_strict),
    }
)


@automation.register_action(
    "a76xx.send_ussd", A76XXSendUssdAction, A76XX_SEND_USSD_SCHEMA
)
async def a76xx_send_ussd_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_USSD], args, cg.std_string)
    cg.add(var.set_ussd(template_))
    return var


@automation.register_action(
    "a76xx.disconnect",
    A76XXDisconnectAction,
    cv.Schema({cv.GenerateID(): cv.use_id(A76XXComponent)}),
)
async def a76xx_disconnect_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    return var
