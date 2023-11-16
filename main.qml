import QtQuick
import QtQuick.Controls.Basic
ApplicationWindow {
    id:rootWindow
    visible: true
    width: 486
    height: 495
    title: "Weather"
    x:  12
    y: screen.desktopAvailableHeight - height - 48
    flags: Qt.FramelessWindowHint | Qt.Window
    property QtObject container
    MouseArea
    {
        id: mouseArea
        anchors.fill: parent
        property variant clickPos: "1,1"
        onPressed:(mouse) => 
        {
        clickPos  = Qt.point(mouse.x,mouse.y)
        }
        onPositionChanged: (mouse) => 
        {
        var delta = Qt.point(mouse.x-clickPos.x, mouse.y-clickPos.y)
        rootWindow.x += delta.x;
        rootWindow.y += delta.y;
        }
    }
    property string temp: "0"
    property QtObject backend
    Rectangle{
        
        anchors.fill: parent
        Image
        {
            anchors.fill: parent
            source: "./GITHUBPFP"
            fillMode: Image.PreserveAspectCrop
        }
        
        color: "dark grey"
            Text {
                anchors {
                        top: parent.top
                        topMargin: 20
                        bottomMargin: 12
                        left: parent.left
                        leftMargin: 12
                        }
                font
                {
                    
                    weight: 600
                    italic: true
                }
            text: temp
            font.pixelSize: 24
            color: "white"
            style: "Raised","Outline"
            styleColor: "black"
        }

        Button
        {
            onClicked: Qt.quit()
            icon.color:"black"
            implicitWidth:50
            implicitHeight:25
            text:"EXIT"
            font
            {
                
                weight: 600
                italic: true
            }
            anchors
            {
            bottom: parent.bottom
            bottomMargin: 12
            right: parent.right
            rightMargin: 12
            }
        }
        Row
        {
            spacing: 0
            anchors
                {
                    bottom: parent.bottom
                    bottomMargin: 12
                    left: parent.left
                    leftMargin: 12
                }
            TextField
            {
                id:cityText
                placeholderText: qsTr("Enter New Location") 
                text:""
                color: activeFocus ? "Black":"Grey"
            }
            Button
            {
                onClicked:
                {
                    //cityText.text="DAVE"
                    backend.text(cityText.text)
                } 
                icon.color:"black"
                implicitWidth:50
                implicitHeight:cityText.height
                text:"Enter"
                font
                {
                    
                    weight: 600
                    italic: true
                }
            }
    
    
    
    }
    Connections {
        target: backend
        function onUpdated(msg) 
        {
        temp = msg;
        }
    }
    
}
}