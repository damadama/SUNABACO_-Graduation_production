


$("#img_submit_btn").click(function(){
    // ファイルデータ
    const file = document.getElementById("submit_img").files[0];
    // フォームデータを作成
    const formData = new FormData();
    // avatarというフィールド名でファイルを追加
    formData.append("avatar", file);
    // アップロード
    fetch("C:\Users\windu\Desktop\workspace\flask_test\images", { method: "POST", body: formData });
});


// ここから防犯マップにて追記
// No1のmap表示
// function GetMap() {
//     const map = new Microsoft.Maps.Map('#myMap', {
//         center: new Microsoft.Maps.Location(47.6149, -122.1941), //Location center position
//         mapTypeId: Microsoft.Maps.MapTypeId.load, //Type: [load, aerial,canvasDark,canvasLight,birdseye,grayscale,streetside]
//         zoom: 15  //Zoom:1=zoomOut, 20=zoomUp[ 1~20 ]
//     });
// }
