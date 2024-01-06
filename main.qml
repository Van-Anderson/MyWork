import QtQuick
import QtQuick.Controls.Basic


ApplicationWindow {
    id:rootWindow
    visible: true
    width: screen.width/4
    height: screen.height/2.5
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
            source: "./Background"
            fillMode: Image.PreserveAspectCrop
        }
        Button
        {
            anchors{
                top:parent.top
                right: parent.right
                topMargin: 5
                rightMargin: 5

            }
            implicitWidth:25
            implicitHeight:25
            Image
            {
                anchors.fill: parent
                source: "./SettingIcon.PNG"
                fillMode: Image.PreserveAspectCrop
            }
            onClicked:dialog.open()
        }
        Dialog {
            id: dialog
            title: "Settings"
            standardButtons: Dialog.Ok | Dialog.Cancel
            Column
            {
            Text
            {
                text: "Openweathermap API key:"
                color: "black"
            }
            TextField
            {
                width:parent.length
                id:settingsInput
                placeholderText: qsTr("API Key") 
                text:""
                color: activeFocus ? "Black":"Grey"
            }
            }
            
            
            onAccepted: backend.updateAPI(settingsInput.text)
            onRejected: console.log("Cancel clicked")
            }

        color: "dark grey"
            Text {
                width: rootWindow.width-15
                wrapMode: Text.WordWrap
                fontSizeMode: Text.Fit
                minimumPixelSize: 20
                anchors {
                        top: parent.top
                        topMargin: 20
                        bottomMargin: 0
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
                width:70
                id:cityText
                placeholderText: qsTr("City") 
                text:""
                color: activeFocus ? "Black":"Grey"
            }
            TextField
            {
                width:70
                id:userStateText
                placeholderText: qsTr("State") 
                text:""
                color: activeFocus ? "Black":"Grey"
            }
            TextField
            {
                width:70
                id:countryText
                placeholderText: qsTr("Country") 
                text:""
                color: activeFocus ? "Black":"Grey"
            }
            Button
            {
                width:90
                onClicked:
                {
                    
                    backend.updateCity(cityText.text, userStateText.text,countryText.text)
                    cityText.text=""
                    userStateText.text=""
                    countryText.text=""
                } 
                icon.color:"black"
                implicitWidth:50
                implicitHeight:cityText.height
                text:"Update City"
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