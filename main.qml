import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    id: mainWindow
    width: 200
    height: 200
    visible: true
    
    // Transparent Window Setup
    color: "transparent"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
    
    property string currentState: "idle"
    property bool moving: false

    // CONNECTION TO PYTHON
    Connections {
        target: backend
        function onIsMoving(isMoving) { moving = isMoving }
        function onStateChanged(newState) { currentState = newState }
        function onMovePet(targetX, targetY) { 
            mainWindow.x = targetX
            mainWindow.y = targetY 
        }
        function onRequestPosition() { 
            backend.set_home_location(mainWindow.x, mainWindow.y) 
        }
    }

    // --- FIX: DISABLE ANIMATION WHILE DRAGGING ---
    // If we are dragging, 'enabled' becomes false, so x/y update instantly.
    // If we are NOT dragging, 'enabled' is true, so it glides smoothly.
    Behavior on x { 
        enabled: !dragArea.pressed 
        NumberAnimation { duration: 2000; easing.type: Easing.InOutQuad } 
    }
    Behavior on y { 
        enabled: !dragArea.pressed
        NumberAnimation { duration: 2000; easing.type: Easing.InOutQuad } 
    }

    Rectangle {
        id: orb
        width: 100
        height: 100
        radius: 50
        anchors.centerIn: parent
        border.color: "lightgray"
        border.width: 2
        state: currentState
        
        states: [
            State { name: "idle"; PropertyChanges { target: orb; color: "#ffffff" } },
            State { name: "browse"; PropertyChanges { target: orb; color: "#ff8c00" } },
            State { name: "music"; PropertyChanges { target: orb; color: "#1db954" } },
            State { name: "coding"; PropertyChanges { target: orb; color: "#8000d2ff" } },
            State { name: "Design"; PropertyChanges { target:orb; color: "#78ff02ff"} },
            State { name: "stressed"; PropertyChanges { target: orb; color: "red" } }
        ]

        Behavior on color { ColorAnimation { duration: 500 } }

        // WALKING ANIMATION (Bobbing)
        SequentialAnimation {
            // Run if moving AND NOT dragging
            running: moving && !dragArea.pressed
            loops: Animation.Infinite
            
            NumberAnimation { target: orb; property: "anchors.verticalCenterOffset"; to: -10; duration: 250; easing.type: Easing.InOutSine }
            NumberAnimation { target: orb; property: "anchors.verticalCenterOffset"; to: 0; duration: 250; easing.type: Easing.InOutSine }
        }

        // OTHER ANIMATIONS (Idle, Music, etc.)
        SequentialAnimation {
            running: currentState === "idle" || currentState === "browse"
            loops: Animation.Infinite
            alwaysRunToEnd: true
            NumberAnimation { target: orb; property: "scale"; to: 0.95; duration: 2000; easing.type: Easing.InOutQuad }
            NumberAnimation { target: orb; property: "scale"; to: 1.05; duration: 2000; easing.type: Easing.InOutQuad }
        }
        SequentialAnimation {
            running: currentState === "music"
            loops: Animation.Infinite
            NumberAnimation { target: orb; property: "anchors.verticalCenterOffset"; to: -20; duration: 300; easing.type: Easing.OutQuad }
            NumberAnimation { target: orb; property: "anchors.verticalCenterOffset"; to: 0; duration: 300; easing.type: Easing.OutBounce }
        }
        SequentialAnimation {
            running: currentState === "coding"
            loops: Animation.Infinite
            PropertyAnimation { target: orb; property: "color"; to: "#E600d2ff"; duration: 800 }
            PropertyAnimation { target: orb; property: "color"; to: "#8000d2ff"; duration: 800 }
        }
        SequentialAnimation {
            running: currentState === "stressed"
            loops: Animation.Infinite
            NumberAnimation { target: orb; property: "anchors.horizontalCenterOffset"; to: -5; duration: 50 }
            NumberAnimation { target: orb; property: "anchors.horizontalCenterOffset"; to: 5; duration: 50 }
        }
        SequentialAnimation {
            running: currentState === "Design"
            loops: Animation.Infinite
            NumberAnimation { target: orb; property: "anchors.horizontalCenterOffset"; to: -5; duration: 50 }
            NumberAnimation { target: orb; property: "anchors.horizontalCenterOffset"; to: 5; duration: 50 }
        }
    }

    // DRAGGABLE LOGIC
    MouseArea {
        id: dragArea // Give it an ID so we can check 'dragArea.pressed'
        anchors.fill: parent
        property point lastMousePos
        
        onPressed: { 
            // 1. Tell Python to PAUSE Logic
            backend.start_drag()
            lastMousePos = Qt.point(mouseX, mouseY); 
        }

        onReleased: {
            // 2. Tell Python to RESUME Logic
            backend.end_drag()
        }

        onPositionChanged: {
            var deltaX = mouseX - lastMousePos.x;
            var deltaY = mouseY - lastMousePos.y;
            mainWindow.x += deltaX;
            mainWindow.y += deltaY;
        }
    }
}