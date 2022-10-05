// 1 グローバルメニューを多言語対応
// 日本語と英語でよい　（ヘッダーメニューのみでok）

// メニューに、言語を切り替えるボタンを配置し
// 押すとメニューが英語⇒日本語相互切り替わるように

$("#japanese").click(function(){
    $("#headline_area").text("見出しのエリア");
    $("#flex_area").text("flexのエリア");
    $("#centering_area").text("センタリングエリア");
    $("#production_result").text("制作実績");
});

$("#english").click(function(){
    $("#headline_area").text("Heading");
    $("#flex_area").text("Flex");
    $("#centering_area").text("Centering");
    $("#production_result").text("Product");
});


// 2 3角形の面積を求めよ
// 引数を2つ渡すと、3角形の面積を計算し、
// 結果をコンソールに出力せよ

var width =4
var height =6

function menseki(width,height){
    return (width+height)/2;
}

console.log("三角形の面積："+menseki(width,height));

// 3　製作実績画像サイズ拡大
$("#img_big").click(function(){
    $(".portfolio_img").css('width','600px');
});

// 4　製作実績の画像を変更する
$("#img_change").click(function(){
    $(".portfolio_img").attr('src', 'img/neko.jpg');
});

// 5 ブロックエリアをボタンで追加する
$("#block_add").click(function(){
    $(".flex_area").css('flex-wrap', 'wrap');
    $(".flex_area").append("<div><h2>flexを使って左から詰めていく</h2><p>ここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります</p></div>");
});

// 6 ブロックエリアを任意の数追加する
$("#fig_submit").click(function(e){
    e.preventDefault();  // ボタン押下時のサブミット動作を抑制
    var j = $("#block_add_fig").val();
    
    for(var i=1; i<=j; i++){
        $(".flex_area").css('flex-wrap', 'wrap');
        $(".flex_area").append("<div><h2>flexを使って左から詰めていく</h2><p>ここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入りますここにflexに関してのテキストが入ります</p></div>");        
    }
});


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
function GetMap() {
    const map = new Microsoft.Maps.Map('#myMap', {
        center: new Microsoft.Maps.Location(47.6149, -122.1941), //Location center position
        mapTypeId: Microsoft.Maps.MapTypeId.load, //Type: [load, aerial,canvasDark,canvasLight,birdseye,grayscale,streetside]
        zoom: 8  //Zoom:1=zoomOut, 20=zoomUp[ 1~20 ]
    });
}