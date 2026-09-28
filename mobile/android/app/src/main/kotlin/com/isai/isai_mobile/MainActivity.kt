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
                        val cleanNum = phoneNumber.replace(Regex("[^0-9+]"), "")
                        val uriStr = if (cleanNum.isNotEmpty()) "tel:$cleanNum" else "tel:$phoneNumber"
                        val intent = Intent(Intent.ACTION_DIAL).apply {
                            data = Uri.parse(uriStr)
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
                    val appQuery = call.argument<String>("packageName") ?: ""
                    try {
                        val appMap = mapOf(
                            "whatsapp" to "com.whatsapp",
                            "youtube" to "com.google.android.youtube",
                            "chrome" to "com.android.chrome",
                            "spotify" to "com.spotify.music",
                            "instagram" to "com.instagram.android",
                            "maps" to "com.google.android.apps.maps",
                            "gmail" to "com.google.android.gm"
                        )

                        val resolvedPkg = appMap[appQuery.lowercase().trim()] ?: appQuery

                        var launchIntent = packageManager.getLaunchIntentForPackage(resolvedPkg)

                        if (launchIntent == null) {
                            val installed = packageManager.getInstalledApplications(0)
                            for (app in installed) {
                                val label = packageManager.getApplicationLabel(app).toString().lowercase()
                                if (label.contains(appQuery.lowercase()) || app.packageName.lowercase().contains(appQuery.lowercase())) {
                                    launchIntent = packageManager.getLaunchIntentForPackage(app.packageName)
                                    if (launchIntent != null) break
                                }
                            }
                        }

                        if (launchIntent != null) {
                            startActivity(launchIntent)
                            result.success(true)
                        } else {
                            result.error("APP_NOT_FOUND", "Application $appQuery is not installed", null)
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
