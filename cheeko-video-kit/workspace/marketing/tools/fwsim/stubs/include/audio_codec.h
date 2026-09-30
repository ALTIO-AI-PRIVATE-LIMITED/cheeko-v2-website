#pragma once
class AudioCodec {
public:
  int output_volume() const { return 70; }
  int output_sample_rate() const { return 24000; }
  int input_sample_rate() const { return 16000; }
  bool output_enabled() const { return true; }
  void SetOutputVolume(int) {}
  void EnableOutput(bool) {}
  void EnableInput(bool) {}
};
