const { Bodies, Body, Composite, Engine, Events, Render, Runner, Sleeping } =
  Matter;

const WIDTH = 640; // 横幅
const HEIGHT = 680; // 高さ
const WALL_T = 10; // 壁の厚さ
const DEADLINE = 635; // ゲームオーバーになる高さ
const FRICTION = 0.3; // 摩擦
const MASS = 1; // 重量
const MAX_LEVEL = 11;
const WALL_COLOR = "#008080";
const BUBBLE_COLORS = {  //色変更
  0: "#8b0000",   // DarkRed
  1: "#ff69b4",   // MediumVioletRed
  2: "#9400d3",   // DarkViolet
  3: "#f4a460",   // SandyBrown
  4: "#ff8c00",   // DarkOrange
  5: "#ff0000",   // Red
  6: "#f0e68c",   // Khaki
  7: "#ffb6c1",   // LightPink
  8: "#ffff00",   // Yellow
  9: "#3cb371",   // MediumSeaGreen
  10: "#006400",  // DarkGreen
};

const OBJECT_CATEGORIES = {
  WALL: 0x0001,
  BUBBLE: 0x0002,
  BUBBLE_PENDING: 0x0004,
};

class BubbeGame {
  engine;
  render;
  runner;
  currentBubble = undefined;
  score;
  scoreChangeCallBack;
  gameover = false;
  defaultX = WIDTH / 2;
  message;

  constructor(container, message, scoreChangeCallBack) {
    this.message = message;
    this.scoreChangeCallBack = scoreChangeCallBack;
    this.engine = Engine.create({
      constraintIterations: 3
    });
    this.render = Render.create({
      element: container,
      engine: this.engine,
      options: {
        width: WIDTH,
        height: HEIGHT,
        wireframes: false,
      },
    });
    this.runner = Runner.create();
    Render.run(this.render);
    container.addEventListener("click", this.handleClick.bind(this));
    container.addEventListener("mousemove", this.handleMouseMove.bind(this));
    Events.on(this.engine, "collisionStart", this.handleCollision.bind(this));
    Events.on(this.engine, "afterUpdate", this.checkGameOver.bind(this));
  }

  init() {
    // リセット時も使うので一旦全部消す
    Composite.clear(this.engine.world);
    this.resetMessage();

    // 状態初期化
    this.gameover = false;
    this.setScore(0);

    // 地面と壁作成
    // 矩形の場合X座標、Y座標、横幅、高さの順に指定、最後にオプションを設定できる
    const ground = Bodies.rectangle(
      WIDTH / 2,
      HEIGHT - WALL_T / 2,
      WIDTH,
      WALL_T,
      {
        isStatic: true,
        label: "ground",
        render: {
          fillStyle: WALL_COLOR,
        },
      }
    );
    const leftWall = Bodies.rectangle(WALL_T / 2, HEIGHT / 2, WALL_T, HEIGHT, {
      isStatic: true,
      label: "leftWall",
      render: {
        fillStyle: WALL_COLOR,
      },
    });
    const rightWall = Bodies.rectangle(
      WIDTH - WALL_T / 2,
      HEIGHT / 2,
      WALL_T,
      HEIGHT,
      {
        isStatic: true,
        label: "rightWall",
        render: {
          fillStyle: WALL_COLOR,
        },
      }
    );
    // 地面と壁を描画
    Composite.add(this.engine.world, [ground, leftWall, rightWall]);
    Runner.run(this.runner, this.engine);

    // ステータスをゲーム準備完了に
    this.gameStatus = "ready";
    this.showReadyMessage();
  }

  start(e) {
    e.preventDefault();
    e.stopPropagation();
    if (this.gameStatus === "ready") {
      this.gameStatus = "canput";
      this.createNewBubble();
      this.resetMessage();
    }
  }

  createNewBubble() {
    if (this.gameover) {
        return;
    }

    // バブルのサイズを制限
    const levels = [0, 1, 2, 3];  // 小さい順に4つのサイズ
    const level = levels[Math.floor(Math.random() * levels.length)];  // ランダムに選択

    const radius = level * 10 + 20;  // サイズに対応する半径

    // 描画位置のX座標、y座標、円の半径を渡す
    const currentBubble = Bodies.circle(this.defaultX, 30, radius, {
        isSleeping: true,
        label: "bubble_" + level,
        friction: FRICTION,
        mass: MASS,
        collisionFilter: {
            group: 0,
            category: OBJECT_CATEGORIES.BUBBLE_PENDING,
            mask: OBJECT_CATEGORIES.WALL | OBJECT_CATEGORIES.BUBBLE,
        },
        render: {
            fillStyle: BUBBLE_COLORS[level],
            lineWidth: 1,
        },
    });

    this.currentBubble = currentBubble;
    Composite.add(this.engine.world, [currentBubble]);
}


  putCurrentBubble() {
    if (this.currentBubble) {
      Sleeping.set(this.currentBubble, false);
      this.currentBubble.collisionFilter.category = OBJECT_CATEGORIES.BUBBLE;
      this.currentBubble = undefined;
    }
  }

  // ゲームオーバー判定
  // 一定以上の高さに上方向の速度を持つオブジェクトが存在している場合ゲームオーバーとする
  checkGameOver() {
    const bubbles = Composite.allBodies(this.engine.world).filter((body) =>
      body.label.startsWith("bubble_")
    );
    for (const bubble of bubbles) {
      if (bubble.position.y < HEIGHT - DEADLINE && bubble.velocity.y < 0) {
        Runner.stop(this.runner);
        this.gameover = true;
        this.showGameOverMessage();
        break;
      }
    }
  }

  // ゲーム開始前のメッセージを表示する

  
//game開始前の設定：gameに支障は無い
showReadyMessage() {
  // メッセージ表示のテキスト作成
  const p = document.createElement("p");
  p.classList.add("mainText");
  p.textContent = "箱の上に球体を落として同じ種類の球体をつなげていくゲーム";

  const p2 = document.createElement("p");
  p2.classList.add("subText");
  p2.textContent = "同じ円を合わせて大きくするゲーム";

  // 「Start」ボタン作成
  const button = document.createElement("button");
  button.setAttribute("type", "button");
  button.classList.add("button");
  button.addEventListener("click", this.start.bind(this));
  button.innerText = "Start";

  // メッセージにテキストとボタン追加
  this.message.appendChild(p);
  this.message.appendChild(p2);
  this.message.appendChild(button);

  this.message.style.display = "block";
}


  // gameoverともう一度　：ゲームに支障は無い
showGameOverMessage() {
  // メッセージに表示するテキストを作成
  const p = document.createElement("p");
  p.classList.add("mainText");
  p.textContent = "Game Over";

  const p2 = document.createElement("p");
  p2.classList.add("subText");
  p2.textContent = `Score: ${this.score}`;

  // 「もう一度」ボタン作成
  const button = document.createElement("button");
  button.setAttribute("type", "button");
  button.classList.add("button");
  button.addEventListener("click", this.init.bind(this));
  button.innerText = "もう一度";

  // メッセージにテキストとボタンを追加
  this.message.appendChild(p);
  this.message.appendChild(p2);
  this.message.appendChild(button);

  // メッセージ表示
  this.message.style.display = "block";
}


  resetMessage() {
    this.message.replaceChildren();
    this.message.style.display = "none";
  }

  handleClick() {
    if (this.gameover) {
      return;
    }
    if (this.gameStatus === "canput") {
      this.putCurrentBubble();
      this.gameStatus = "interval";
      setTimeout(() => {
        this.createNewBubble();
        this.gameStatus = "canput";
      }, 500);
    }
  }

  // 衝突が発生したときの処理
handleCollision({ pairs }) {
  for (const pair of pairs) {
    const { bodyA, bodyB } = pair;

    // 既に衝突して消滅済みのバブルについての判定だった場合はスキップ
    if (
      !Composite.get(this.engine.world, bodyA.id, "body") ||
      !Composite.get(this.engine.world, bodyB.id, "body")
    ) {
      continue;
    }

    // 衝突した物体が同じバブルであり、かつバブルのラベルが対応している場合
    if (bodyA.label === bodyB.label && bodyA.label.startsWith("bubble_")) {
      const currentBubbleLevel = Number(bodyA.label.substring(7));

      // スコア加算
      this.setScore(this.score + 2 ** currentBubbleLevel);

      // 最大サイズの場合は新たなバブルは生まれない
      if (currentBubbleLevel === 11) {
        Composite.remove(this.engine.world, [bodyA, bodyB]);
        continue;
      }

      // 新しいバブルのサイズや位置を計算して作成
      const newLevel = currentBubbleLevel + 1;
      const newX = (bodyA.position.x + bodyB.position.x) / 2;
      const newY = (bodyA.position.y + bodyB.position.y) / 2;
      const newRadius = newLevel * 10 + 20;

      const newBubble = Bodies.circle(newX, newY, newRadius, {
        label: "bubble_" + newLevel,
        friction: FRICTION,
        mass: MASS,
        collisionFilter: {
          group: 0,
          category: OBJECT_CATEGORIES.BUBBLE,
          mask: OBJECT_CATEGORIES.WALL | OBJECT_CATEGORIES.BUBBLE,
        },
        render: {
          fillStyle: BUBBLE_COLORS[newLevel],
          lineWidth: 1,
        },
      });

      // 古いバブルを削除し、新しいバブルを追加
      Composite.remove(this.engine.world, [bodyA, bodyB]);
      Composite.add(this.engine.world, [newBubble]);
    }
  }
}

  handleMouseMove(e) {
    // ゲームの状態が"canput"でないか、バブルが存在しない場合は処理を終了
    if (this.gameStatus !== "canput" || !this.currentBubble) {
      return;
    }
  
    //X座標
    const { offsetX } = e;
  
    // バブル半径
    const currentBubbleRadius =
      Number(this.currentBubble.label.substring(7)) * 10 + 20;
  
    // 新しいX座標を計算し、最小値と最大値を設定　　いじらないで
    const newX = Math.max(
      Math.min(offsetX, WIDTH - 10 - currentBubbleRadius),
      10 + currentBubbleRadius
    );
  
    // 新X座標
    Body.setPosition(this.currentBubble, {
      x: newX,
      y: this.currentBubble.position.y,
    });
  
    // 初期X座標更新
    this.defaultX = newX;
  }
  

  setScore(score) {
    this.score = score;
    if (this.scoreChangeCallBack) {
      this.scoreChangeCallBack(score);
    }
  }
}

// ウィンドウ完全読み込み処理
window.onload = () => {
  // HTML内
  const container = document.querySelector(".container");
  const message = document.querySelector(".message");

  // スコア表示の要素作成
  const scoreElement = document.createElement("div");
  scoreElement.classList.add("score");
  
  // body要素にスコア表示要素追加
  document.body.appendChild(scoreElement);

  // スコア変更時のコールバック関数
  const onChangeScore = (val) => {
    scoreElement.textContent = `スコア: ${val}`;
  };

  const game = new BubbeGame(container, message, onChangeScore);

  // ゲームの初期化
  game.init();

  // スコアの要素にスタイルを設定
  scoreElement.style.position = "absolute";
  scoreElement.style.top = "10px";
  scoreElement.style.right = "20px"; // 右の余白を調整
  scoreElement.style.fontSize = "20px"; // フォントサイズを大きく

  // Start ボタンのスタイルを設定
  const startButton = document.querySelector(".button");
  startButton.style.fontSize = "18px"; // フォントサイズを大きく
  startButton.style.padding = "10px 20px"; // パディングを調整

  // ゲームオーバーメッセージ内の「もう一度」ボタンのスタイルを設定
  const restartButton = document.querySelector(".message button");
  restartButton.style.fontSize = "18px"; // フォントサイズを大きく
  restartButton.style.padding = "10px 20px"; // パディングを調整

  const bgm = document.getElementById('bgm'); // 新しいaudio要素を取得

  // BGMが読み込まれたら再生を開始
  bgm.addEventListener('canplaythrough', () => {
    bgm.play();
  });

  // ゲームが初期化されたときに再生を開始
  game.initCallback = () => {
    bgm.play();
  };
};
