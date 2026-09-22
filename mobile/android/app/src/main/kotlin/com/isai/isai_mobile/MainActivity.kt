package com.isai.isai_mobile

import android.content.Intent
import android.net.Uri
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val CHANNEL = "com.isai.mobile/device_control"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "makePhoneCall" -> {
                    val phoneNumber = call.argument<String>("phoneNumber") ?: ""
                    try {
                        val intent = Intent(Intent.ACTION_DIAL).apply {
                            data = Uri.parse("tel:$phoneNumber")
                        }
                        startActivity(intent)
                        result.success(true)
                    } catch (e: Exception) {
                        result.error("CALL_FAILED", e.message, null)
                    }
                }
                "openWebSearch" -> {
                    val query = call.argument<String>("query") ?: ""
                    try {
                        val intent = Intent(Intent.ACTION_VIEW).apply {
                            data = Uri.parse("https://www.google.com/search?q=${Uri.encode(query)}")
                        }
                        startActivity(intent)
                        result.success(true)
                    } catch (e: Exception) {
                        result.error("SEARCH_FAILED", e.message, null)
                    }
                }
                "launchApp" -> {
                    val packageName = call.argument<String>("packageName") ?: ""
                    try {
                        val launchIntent = packageManager.getLaunchIntentForPackage(packageName)
                        if (launchIntent != null) {
                            startActivity(launchIntent)
                            result.success(true)
                        } else {
                            result.error("APP_NOT_FOUND", "Application $packageName is not installed", null)
                        }
                    } catch (e: Exception) {
                        result.error("LAUNCH_FAILED", e.message, null)
                    }
                }
                else -> result.notImplemented()
            }
        }
    }
}
