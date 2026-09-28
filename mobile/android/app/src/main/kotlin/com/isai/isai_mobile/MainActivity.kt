package com.isai.isai_mobile

import android.content.Intent
import android.net.Uri
import android.provider.ContactsContract
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val CHANNEL = "com.isai.mobile/device_control"

    private fun lookupContactNumber(nameQuery: String): String? {
        try {
            val uri = ContactsContract.CommonDataKinds.Phone.CONTENT_URI
            val projection = arrayOf(
                ContactsContract.CommonDataKinds.Phone.NUMBER,
                ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME
            )
            val selection = "${ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME} LIKE ?"
            val selectionArgs = arrayOf("%$nameQuery%")
            val cursor = contentResolver.query(uri, projection, selection, selectionArgs, null)
            cursor?.use {
                if (it.moveToFirst()) {
                    val numberIndex = it.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER)
                    if (numberIndex != -1) {
                        return it.getString(numberIndex)
                    }
                }
            }
        } catch (e: Exception) {
            // Permission or cursor exception fallback
        }
        return null
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            when (call.method) {
                "makePhoneCall" -> {
                    val targetInput = call.argument<String>("phoneNumber") ?: ""
                    try {
                        var dialNumber = targetInput.replace(Regex("[^0-9+]"), "")

                        if (dialNumber.length < 3) {
                            // Target input is a contact name (e.g. "Ammi", "Mom", "John")
                            val lookedUpNum = lookupContactNumber(targetInput)
                            if (lookedUpNum != null) {
                                dialNumber = lookedUpNum.replace(Regex("[^0-9+]"), "")
                            }
                        }

                        val uriStr = if (dialNumber.isNotEmpty()) "tel:$dialNumber" else "tel:$targetInput"
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
