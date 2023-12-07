#pragma once

#include "esphome/core/component.h"
#include "esphome/components/output/float_output.h"
#include "esphome/components/i2c/i2c.h"

namespace esphome {
namespace seesaw {

class SeeSawOutput;

class SeeSawChannel : public output::FloatOutput {
 public:
  void set_channel(uint8_t channel) { channel_ = channel; }
  void set_parent(SeeSawOutput *parent) { parent_ = parent; }

 protected:
  friend class SeeSawOutput;

  void write_state(float state) override;

  uint8_t channel_;
  SeeSawOutput *parent_;
};

/// PCA9685 float output component.
class SeeSawOutput : public Component, public i2c::I2CDevice {
 public:
  SeeSawOutput(uint8_t mode = 0) : mode_(mode) {}

  void register_channel(SeeSawChannel *channel);

  void setup() override;
  void dump_config() override;
  float get_setup_priority() const override { return setup_priority::HARDWARE; }
  void loop() override;
  void set_extclk(bool extclk) { this->extclk_ = extclk; }
  void set_frequency(float frequency) { this->frequency_ = frequency; }

 protected:
  friend SeeSawChannel;

  void set_channel_value_(uint8_t channel, uint16_t value) {
    if (this->pwm_amounts_[channel] != value)
      this->update_ = true;
    this->pwm_amounts_[channel] = value;
  }

  float frequency_;
  uint8_t mode_;
  bool extclk_ = false;

  uint8_t min_channel_{0xFF};
  uint8_t max_channel_{0x00};
  uint16_t pwm_amounts_[16] = {
      0,
  };
  bool update_{true};
};

}  // namespace pca9685
}  // namespace esphome
