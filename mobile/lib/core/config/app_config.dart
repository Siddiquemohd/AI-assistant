import 'package:flutter/foundation.dart';

class AppConfig {
  // Toggle to true to connect to the deployed Render backend
  static const bool useProductionBackend = true;
  static const String productionApiBaseUrl = 'https://isai-backend.onrender.com/api/v1';

  static String get apiBaseUrl {
    if (useProductionBackend) {
      return productionApiBaseUrl;
    }
    if (kIsWeb) {
      return 'http://localhost:8000/api/v1';
    } else if (defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:8000/api/v1';
    } else {
      return 'http://localhost:8000/api/v1';
    }
  }

  static const Duration timeout = Duration(seconds: 30);
}
