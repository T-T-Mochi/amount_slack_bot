/**
 * @author Tada Tomoya
 * @version 2.0.1
 */
 
int colorhWidth= 0;
int rectHight = 100;
int rectWidth = 400;
int rectx = 40;
int recty = 70;

int percent = 0;

String percentString;

void settings(){
  size(480, 250);
}


/**
 * setupメソッド
 * セットアップ
 * @param なし
 */
void setup(){
  background(255,255,255);
  colorMode(RGB,256);
  
  //PFont font = createFont("Osaka",32,true);
  //stextFont(font);// 選択したフォントを使用する
  
  //
  
  percent = 100; //ここにパーセントの値を渡したら適した表示ができる
  
}

/**
 * drawメソッド
 * 描画を行う
 * @param なし
 */
void draw(){
  background(255,255,255);
  printText(percent);

  strokeWeight(3);
  fill(255,255,255);
  rect(rectx, recty, rectWidth, rectHight);
  strokeWeight(3);

  changeColor(percent);
  colorhWidth = toWidth(percent);
  rect(rectx, recty, colorhWidth, rectHight);
}


/**
 * changeColorメソッド
 * 計算した割合に応じて表示する色を変える
 * @param percent 色を表示する割合
 */
void changeColor(double percent){
  //100-(識別したい%の値)と計算したパーセンテージを比較することで、識別が可能
  if(percent > 50){
    fill(0,255,0);
  }
  else if(percent > 20){
    fill(255,255,0);
  } 
  else {
    fill(255,0,0);
  }
}

/**
 * accountPercentメソッド
 * 色を表示するパーセントの計算
 * @param index 色を表示する横の長さ
 */
double accountPercent(int colorhWidth){
  return ((double)colorhWidth) * rectHight / rectWidth;
}

/**
 * toWidthtメソッド
 * パーセントから色をつけた四角形の横の長さを求める
 * @param percent 色を表示したいエリアのパーセント
 */
int toWidth(double percent){
  return (int)percent * rectWidth / rectHight;
}

/**
 * printTextメソッド
 * 黒影のある文字の表示
 * @param percent 表示させるパーセントの数字
 **/
void printText(double percent){
  String percentString = String.valueOf(percent) + "%";
  
  fill(0);
  textSize(33);  // フォントの表示サイズ
  text(percentString, 182, 54);
  
  changeColor(percent);
  textSize(32);  // フォントの表示サイズ
  text(percentString, 185, 55);
}

void keyPressed() {
  println(key);
  if (key == 'a') { 
      if(percent < 100){
        save("./image_data/"+percent+".png");
        println("Up");
        percent = percent + 1;
      }
  } 
  else if (key == 'd') { 
     if(percent > -1){
       save("./image_data/"+percent+".png");
       println("down");
        percent = percent - 1;
      }
  } 
}
