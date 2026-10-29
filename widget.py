"""
widget.py - UniFlow Floating Desktop Overlay Widget (Minimalist Edition)
A clean, minimal, native macOS floating widget:
- Pure matte black background with subtle 1px border (#222222)
- No loud green borders; sleek, understated aesthetic matching modern macOS utilities
- Embedded official green neon integral logo
- Top-right corner of screen (NSStatusWindowLevel)
- Drag to reposition anywhere
- Collapsed: 50x50 clean filleted square
- Expanded: Minimalist status card with Pause/Resume toggle, Quit UniFlow, and terminal tip
"""

import sys
import os
import time
import base64
import subprocess
import ipc

try:
    # pyrefly: ignore[missing-import]
    import AppKit
    # pyrefly: ignore[missing-import]
    import objc
    # pyrefly: ignore[missing-import]
    from Foundation import NSObject, NSPoint, NSRect, NSSize, NSTimer, NSData
except ImportError:
    AppKit = None

LOGO_PNG_BASE64 = """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"""

if AppKit:
    class WidgetView(AppKit.NSView):
        def initWithFrame_(self, frame):
            self = objc.super(WidgetView, self).initWithFrame_(frame)
            if self:
                self.expanded = False
                self.tracking_area = None
                self.is_hovered = False
                raw_data = base64.b64decode(LOGO_PNG_BASE64)
                ns_data = NSData.dataWithBytes_length_(raw_data, len(raw_data))
                self.logo_img = AppKit.NSImage.alloc().initWithData_(ns_data)
                self.drag_start_screen = None
                self.drag_start_origin = None
                self.is_dragging = False
                self.is_paused = False
                self.parent_pid = None
            return self

        def updateTrackingAreas(self):
            objc.super(WidgetView, self).updateTrackingAreas()
            if self.tracking_area:
                self.removeTrackingArea_(self.tracking_area)
            self.tracking_area = AppKit.NSTrackingArea.alloc().initWithRect_options_owner_userInfo_(
                self.bounds(),
                AppKit.NSTrackingMouseEnteredAndExited | AppKit.NSTrackingActiveAlways,
                self,
                None
            )
            self.addTrackingArea_(self.tracking_area)

        def mouseEntered_(self, event):
            self.is_hovered = True
            self.setNeedsDisplay_(True)

        def mouseExited_(self, event):
            self.is_hovered = False
            self.setNeedsDisplay_(True)

        def mouseDown_(self, event):
            self.drag_start_screen = AppKit.NSEvent.mouseLocation()
            self.drag_start_origin = self.window().frame().origin
            self.is_dragging = False

        def mouseDragged_(self, event):
            if self.drag_start_screen and self.drag_start_origin:
                curr = AppKit.NSEvent.mouseLocation()
                dx = curr.x - self.drag_start_screen.x
                dy = curr.y - self.drag_start_screen.y
                if (dx * dx + dy * dy) > 36.0:  # > 6px drag threshold
                    self.is_dragging = True
                    self.window().setFrameOrigin_(NSPoint(self.drag_start_origin.x + dx, self.drag_start_origin.y + dy))

        def mouseUp_(self, event):
            if self.is_dragging:
                self.is_dragging = False
                return
            self.is_dragging = False

            loc = self.convertPoint_fromView_(event.locationInWindow(), None)
            w = self.bounds().size.width
            h = self.bounds().size.height

            if not self.expanded:
                self.window().setExpanded_(True)
            else:
                self.window().setExpanded_(False)

        def drawRect_(self, dirtyRect):
            bounds = self.bounds()
            w = bounds.size.width
            h = bounds.size.height
            is_paused = self.is_paused

            # Subtle rounded card background
            radius = 14.0 if self.expanded else 12.0
            path = AppKit.NSBezierPath.bezierPathWithRoundedRect_xRadius_yRadius_(bounds, radius, radius)
            
            # Deep matte black card
            bg_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.07, 0.07, 0.07, 0.96)
            bg_color.setFill()
            path.fill()

            # Minimal, subtle 1px border (no loud colors)
            border_color = (
                AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.22, 0.22, 0.22, 1.0)
                if not self.is_hovered else
                AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.35, 0.35, 0.35, 1.0)
            )
            border_color.setStroke()
            path.setLineWidth_(1.0)
            path.stroke()

            if not self.expanded:
                # COLLAPSED STATE (50x50)
                if self.logo_img:
                    icon_rect = NSRect(NSPoint(8, 8), NSSize(34, 34))
                    self.logo_img.drawInRect_fromRect_operation_fraction_(
                        icon_rect, NSRect(NSPoint(0, 0), self.logo_img.size()), AppKit.NSCompositingOperationSourceOver, 1.0
                    )

                # Tiny, minimal status indicator dot in top-right
                dot_color = (
                    AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.1, 0.8, 0.4, 0.9)
                    if not is_paused else
                    AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.9, 0.65, 0.2, 0.9)
                )
                dot_path = AppKit.NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(w - 10, h - 10), NSSize(5, 5)))
                dot_color.setFill()
                dot_path.fill()

            else:
                # EXPANDED STATE (200x110)
                # Header Logo + Title
                if self.logo_img:
                    self.logo_img.drawInRect_fromRect_operation_fraction_(
                        NSRect(NSPoint(14, h - 28), NSSize(18, 18)),
                        NSRect(NSPoint(0, 0), self.logo_img.size()),
                        AppKit.NSCompositingOperationSourceOver, 1.0
                    )

                title_font = AppKit.NSFont.systemFontOfSize_weight_(11.0, AppKit.NSFontWeightBold)
                AppKit.NSString.stringWithString_("UNIFLOW").drawAtPoint_withAttributes_(
                    NSPoint(36, h - 25),
                    {
                        AppKit.NSFontAttributeName: title_font,
                        AppKit.NSForegroundColorAttributeName: AppKit.NSColor.whiteColor()
                    }
                )

                # Minimal Status Pill
                status_text = "ACTIVE" if not is_paused else "PAUSED"
                status_color = (
                    AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.1, 0.8, 0.4, 1.0)
                    if not is_paused else
                    AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.9, 0.65, 0.2, 1.0)
                )
                status_font = AppKit.NSFont.systemFontOfSize_weight_(8.5, AppKit.NSFontWeightBold)
                status_attrs = {AppKit.NSFontAttributeName: status_font, AppKit.NSForegroundColorAttributeName: status_color}
                status_size = AppKit.NSString.stringWithString_(status_text).sizeWithAttributes_(status_attrs)
                
                dot_x = w - status_size.width - 22
                dot_path = AppKit.NSBezierPath.bezierPathWithOvalInRect_(NSRect(NSPoint(dot_x, h - 22), NSSize(5, 5)))
                status_color.setFill()
                dot_path.fill()

                AppKit.NSString.stringWithString_(status_text).drawAtPoint_withAttributes_(
                    NSPoint(w - status_size.width - 14, h - 24), status_attrs
                )

                # Divider line
                div_path = AppKit.NSBezierPath.bezierPath()
                div_path.moveToPoint_(NSPoint(14, h - 36))
                div_path.lineToPoint_(NSPoint(w - 14, h - 36))
                AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.18, 0.18, 0.18, 1.0).setStroke()
                div_path.setLineWidth_(1.0)
                div_path.stroke()

                # Action Guide Instructions
                h1_font = AppKit.NSFont.systemFontOfSize_weight_(9.5, AppKit.NSFontWeightMedium)
                h1_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.85, 0.85, 0.85, 1.0)
                h1_text = "• Press Esc anywhere to " + ("Pause" if not is_paused else "Resume")
                AppKit.NSString.stringWithString_(h1_text).drawAtPoint_withAttributes_(
                    NSPoint(14, 46),
                    {AppKit.NSFontAttributeName: h1_font, AppKit.NSForegroundColorAttributeName: h1_color}
                )

                h2_text = "• Ctrl + C in terminal to Quit"
                h2_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.7, 0.4, 0.4, 1.0)
                AppKit.NSString.stringWithString_(h2_text).drawAtPoint_withAttributes_(
                    NSPoint(14, 28),
                    {AppKit.NSFontAttributeName: h1_font, AppKit.NSForegroundColorAttributeName: h2_color}
                )

                # Minimize / Drag Hint
                drag_font = AppKit.NSFont.systemFontOfSize_(7.5)
                drag_color = AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(0.38, 0.38, 0.38, 1.0)
                drag_text = "Click to minimize • Drag to move"
                drag_size = AppKit.NSString.stringWithString_(drag_text).sizeWithAttributes_({AppKit.NSFontAttributeName: drag_font})
                AppKit.NSString.stringWithString_(drag_text).drawAtPoint_withAttributes_(
                    NSPoint((w - drag_size.width) / 2.0, 10),
                    {AppKit.NSFontAttributeName: drag_font, AppKit.NSForegroundColorAttributeName: drag_color}
                )

    class WidgetWindow(AppKit.NSPanel):
        def canBecomeKeyWindow(self):
            return False

        def canBecomeMainWindow(self):
            return False

        def setExpanded_(self, expand):
            collapsed_w, collapsed_h = 50.0, 50.0
            expanded_w, expanded_h = 200.0, 110.0

            curr_frame = self.frame()
            if expand:
                target_w, target_h = expanded_w, expanded_h
                diff_w = target_w - collapsed_w
                new_x = curr_frame.origin.x - diff_w
                new_y = curr_frame.origin.y - (target_h - collapsed_h)
            else:
                target_w, target_h = collapsed_w, collapsed_h
                diff_w = expanded_w - collapsed_w
                new_x = curr_frame.origin.x + diff_w
                new_y = curr_frame.origin.y + (expanded_h - collapsed_h)

            self.contentView().expanded = expand
            self.setFrame_display_animate_(NSRect(NSPoint(new_x, new_y), NSSize(target_w, target_h)), True, True)
            self.contentView().setNeedsDisplay_(True)


class WidgetSyncController(NSObject):
    def updateState_(self, timer):
        if not hasattr(self, "view") or not self.view:
            return

        # Check if parent runner process is still alive
        if hasattr(self, "parent_pid") and self.parent_pid:
            if not ipc.is_process_alive(self.parent_pid):
                print("[UniFlow] Parent runner process terminated. Closing widget.")
                try:
                    self.view.window().close()
                except Exception:
                    pass
                os._exit(0)

        # Sync paused state from session file
        try:
            session = ipc.get_session()
            if session and "paused" in session:
                remote_paused = session["paused"]
                if self.last_paused != remote_paused or self.view.is_paused != remote_paused:
                    self.last_paused = remote_paused
                    self.view.is_paused = remote_paused
                    self.view.setNeedsDisplay_(True)
        except Exception:
            pass


def run_standalone(parent_pid=None):
    if not AppKit:
        print("AppKit not available.")
        return

    if parent_pid is None:
        if "--parent-pid" in sys.argv:
            try:
                idx = sys.argv.index("--parent-pid")
                parent_pid = int(sys.argv[idx + 1])
            except Exception:
                pass
        if parent_pid is None:
            session = ipc.get_session()
            if session:
                parent_pid = session.get("runner_pid")

    ipc.register_widget(os.getpid())

    app = AppKit.NSApplication.sharedApplication()
    app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)

    screen = AppKit.NSScreen.mainScreen()
    vf = screen.visibleFrame()

    collapsed_w, collapsed_h = 50.0, 50.0
    margin_x, margin_y = 24.0, 16.0

    x = vf.origin.x + vf.size.width - collapsed_w - margin_x
    y = vf.origin.y + vf.size.height - collapsed_h - margin_y

    frame = NSRect(NSPoint(x, y), NSSize(collapsed_w, collapsed_h))

    mask = AppKit.NSWindowStyleMaskBorderless | AppKit.NSWindowStyleMaskNonactivatingPanel
    window = WidgetWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        frame, mask, AppKit.NSBackingStoreBuffered, False
    )

    window.setLevel_(AppKit.NSStatusWindowLevel)
    window.setOpaque_(False)
    window.setBackgroundColor_(AppKit.NSColor.clearColor())
    window.setHasShadow_(True)
    window.setCollectionBehavior_(
        AppKit.NSWindowCollectionBehaviorCanJoinAllSpaces |
        AppKit.NSWindowCollectionBehaviorStationary |
        AppKit.NSWindowCollectionBehaviorIgnoresCycle
    )

    view = WidgetView.alloc().initWithFrame_(frame)
    view.parent_pid = parent_pid
    view.is_paused = ipc.get_paused()
    window.setContentView_(view)

    sync_ctrl = WidgetSyncController.alloc().init()
    sync_ctrl.view = view
    sync_ctrl.parent_pid = parent_pid
    sync_ctrl.last_paused = view.is_paused

    NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
        0.1, sync_ctrl, "updateState:", None, True
    )

    window.orderFrontRegardless()
    app.run()


def launch_overlay(parent_pid=None):
    try:
        if parent_pid is None:
            parent_pid = os.getpid()
        if getattr(sys, 'frozen', False):
            # In a PyInstaller bundle, sys.executable is the compiled binary itself
            subprocess.Popen([sys.executable, "--widget", "--parent-pid", str(parent_pid)])
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            widget_script = os.path.join(current_dir, "widget.py")
            subprocess.Popen([sys.executable, widget_script, "--parent-pid", str(parent_pid)], cwd=current_dir)
    except Exception as e:
        print(f"[UniFlow] Could not launch widget overlay: {e}")


if __name__ == "__main__":
    run_standalone()
