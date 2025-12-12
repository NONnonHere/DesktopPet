import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    id: mainWindow
    width: 200
    height: 200
    visible: true
    
    color: "transparent"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint

    Rectangle {
        id: petOrb
        width: 100
        height: 100
        radius: 50 // Makes it a circle
        anchors.centerIn: parent
        
        // Default Color (Blue-ish)
        color: "#00d2ff"
        border.color: "white"
        border.width: 2

        // --- ANIMATIONS ---
        
        // 1. The "Breathing" Animation (Always running)
        SequentialAnimation {
            running: true
            loops: Animation.Infinite
            
            // Scale Up
            NumberAnimation {
                target: petOrb
                property: "scale"
                to: 1.1
                duration: 1000
                easing.type: Easing.InOutQuad
            }
            // Scale Down
            NumberAnimation {
                target: petOrb
                property: "scale"
                to: 1.0
                duration: 1000
                easing.type: Easing.InOutQuad
            }
        }

        // 2. State Logic (Reacting to Python)
        Connections {
            target: backend // Connected to Python's "backend" object
            
            function onStateChanged(newState) {
                if (newState === "coding") {
                    petOrb.color = "#ff8c00" // Orange for Work
                } else if (newState === "stressed") {
                    petOrb.color = "red"     // Red for Alert
                } else if (newState === "music") {
                    petOrb.color = "#0dff00ff" // Green for Spotify
                } else if (newState === "browse") {
                    petOrb.color = "#1db954ff"
                } else {
                    petOrb.color = "#00d2ff" // Blue for Idle
                }
            }
        }
        
        // Allow dragging the window
        MouseArea {
            anchors.fill: parent
            property point lastMousePos
            onPressed: { lastMousePos = Qt.point(mouseX, mouseY); }
            onPositionChanged: {
                var delta = Qt.point(mouseX - lastMousePos.x, mouseY - lastMousePos.y);
                mainWindow.x += delta.x;
                mainWindow.y += delta.y;
            }
        }
    }
}