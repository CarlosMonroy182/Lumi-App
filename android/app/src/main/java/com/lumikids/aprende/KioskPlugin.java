package com.lumikids.aprende;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.Context;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "Kiosk")
public class KioskPlugin extends Plugin {
    private boolean locked(Activity a) {
        ActivityManager am = (ActivityManager) a.getSystemService(Context.ACTIVITY_SERVICE);
        return am != null && am.getLockTaskModeState() != ActivityManager.LOCK_TASK_MODE_NONE;
    }

    @PluginMethod
    public void lock(PluginCall call) {
        Activity a = getActivity();
        a.runOnUiThread(() -> {
            try {
                if (!locked(a)) a.startLockTask();
                call.resolve();
            } catch (Exception e) {
                call.reject(e.getMessage());
            }
        });
    }

    @PluginMethod
    public void unlock(PluginCall call) {
        Activity a = getActivity();
        a.runOnUiThread(() -> {
            try {
                if (locked(a)) a.stopLockTask();
                call.resolve();
            } catch (Exception e) {
                call.reject(e.getMessage());
            }
        });
    }
}
