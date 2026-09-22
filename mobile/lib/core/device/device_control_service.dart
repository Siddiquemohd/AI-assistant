import 'package:flutter/services.dart';

class DeviceControlService {
  static const MethodChannel _channel = MethodChannel('com.isai.mobile/device_control');

  static Future<bool> makePhoneCall(String phoneNumber) async {
    try {
      final bool success = await _channel.invokeMethod('makePhoneCall', {
        'phoneNumber': phoneNumber,
      });
      return success;
    } on PlatformException catch (_) {
      return false;
    }
  }

  static Future<bool> openWebSearch(String query) async {
    try {
      final bool success = await _channel.invokeMethod('openWebSearch', {
        'query': query,
      });
      return success;
    } on PlatformException catch (_) {
      return false;
    }
  }

  static Future<bool> launchApp(String packageName) async {
    try {
      final bool success = await _channel.invokeMethod('launchApp', {
        'packageName': packageName,
      });
      return success;
    } on PlatformException catch (_) {
      return false;
    }
  }
}
