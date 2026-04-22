import random
import time
import sys

def typing_print(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print()

class Player:
    def __init__(self, name, str_pt, agi_pt, tech_pt):
        self.name = name
        self.max_hp = 100
        self.hp = 100
        # 屬性系統
        self.strength = str_pt  # 影響硬碰硬與生存
        self.agility = agi_pt    # 影響躲避率
        self.tech = tech_pt      # 影響拆彈與科技道具
        # 狀態與道具
        self.items = {"伸縮警棍": 1, "閃光彈": 1, "醫療針": 1}
        self.status = "正常"
        self.suspicion = 0 # 隱藏數值：對真相的懷疑度

    def display_ui(self):
        # 視覺化血條
        bar_length = 20
        filled_length = int(bar_length * self.hp / self.max_hp)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        print(f"\n" + "="*40)
        print(f"👤 執法者: {self.name} | 狀態: {self.status}")
        print(f"❤️  HP: [{bar}] {self.hp}/{self.max_hp}")
        print(f"🎒 背包: {', '.join([f'{k}({v})' for k, v in self.items.items() if v > 0])}")
        print(f"📊 屬性: 力量{self.strength} 敏捷{self.agility} 技術{self.tech}")
        print("="*40)

    def check_bleeding(self):
        if self.status == "流血":
            damage = 5
            self.hp -= damage
            print(f"🩸 [警告] 傷口持續流血，HP 減少 {damage}！")

class CyberGame:
    def __init__(self):
        self.p = None

    def setup(self):
        print("⚔️  歡迎來到《暗巷的裁決者：虛空之眼》進階版")
        name = input("輸入你的代號: ")
        print("\n請分配屬性點（總共 10 點，每項最少 1，最多 6）")
        s = int(input("力量 (影響正面衝突): "))
        a = int(input("敏捷 (影響閃避機率): "))
        t = int(input("技術 (影響拆彈/道具): "))
        
        if s + a + t > 10:
            print(">> 偵測到非法黑入，數值重置為平衡型。")
            s, a, t = 3, 3, 4
        self.p = Player(name, s, a, t)

    def combat_roll(self, attribute_value, difficulty):
        # 模擬 D20 骰點系統
        roll = random.randint(1, 20)
        total = roll + attribute_value
        return total >= difficulty, total

    def start(self):
        self.setup()
        
        # --- 場景一 ---
        self.p.display_ui()
        typing_print("【場景一：突襲】")
        typing_print("你追蹤嫌犯進入廢棄工廠。天花板破裂，戴著機械面具的刺客俯衝而下！")
        print("A) 向後翻滾 (敏捷檢定) | B) 警棍架開 (力量檢定) | C) 醫療針 (回血)")
        
        choice = input(">> ").upper()
        if choice == "A":
            success, val = self.combat_roll(self.p.agility, 12)
            if success:
                typing_print(f"✨ 完美躲避！(點數:{val}) 你優雅地側身躲過攻擊。")
            else:
                damage = 15 - self.p.agility
                self.p.hp -= damage
                typing_print(f"💥 動作太慢！(點數:{val}) 刺客劃傷了你的肩膀。 HP -{damage}")
        elif choice == "B":
            success, val = self.combat_roll(self.p.strength, 14)
            if success:
                typing_print(f"💪 硬派抗衡！(點數:{val}) 你架開了短刀並反手一拳！")
            else:
                damage = 30 - self.p.strength
                self.p.hp -= damage
                self.p.status = "流血"
                typing_print(f"😫 全身系統發出哀號！(點數:{val}) 衝擊力讓你受內傷並流血。 HP -{damage}")
        
        # --- 場景二 ---
        self.p.check_bleeding()
        if self.p.hp <= 0: return self.end("死亡：任務失敗")
        self.p.display_ui()
        
        typing_print("【場景二：對峙】")
        typing_print("刺客掏出三枚藍光電子手雷。這不是普通貨色...")
        print("A) 閃光彈反制 (消耗道具) | B) 全速衝刺 (力量/敏捷檢定) | C) 觀察動作 (增加懷疑度)")
        
        choice = input(">> ").upper()
        if choice == "A" and self.p.items["閃光彈"] > 0:
            self.p.items["閃光彈"] -= 1
            typing_print("💡 強光爆發！刺客慘叫一聲，手雷在遠處炸開，你毫髮無傷。")
        elif choice == "B":
            success, _ = self.combat_roll(self.p.agility + self.p.strength, 20)
            if success:
                typing_print("⚡ 極限衝刺！你在手雷引爆前將他撞飛，爆炸在背後發生。 HP-10")
                self.p.hp -= 10
            else:
                typing_print("🔥 躲避不及！你被爆炸衝擊波正面擊中。 HP-40")
                self.p.hp -= 40
        elif choice == "C":
            self.p.suspicion += 50
            self.p.hp -= 20
            typing_print("👁️ 你受傷躲避，但看清了手雷上的標誌...那是執法局的軍用品！(懷疑度上升)")

        # --- 場景三 ---
        self.p.check_bleeding()
        if self.p.hp <= 0: return self.end("死亡：因傷重倒在黎明前")
        self.p.display_ui()

        typing_print("【場景三：終結選擇】")
        typing_print("刺客被逼入牆角，啟動自爆裝置。紅光閃爍，倒數 5 秒...")
        print("A) 拆解晶片 (技術檢定) | B) 踢入深井 (保命) | C) 逼問真相 (懷疑度檢定)")
        
        choice = input(">> ").upper()
        if choice == "A":
            # 技術越高難度越低
            success, val = self.combat_roll(self.p.tech, 18) 
            if success:
                self.end("完美解碼：你阻止了爆炸並獲得了組織名單！")
            else:
                self.p.hp = 0
                self.end("硝煙中的灰燼：你剪錯了線...")
        elif choice == "B":
            self.p.hp -= 10
            self.p.display_ui()
            self.end("墜落的真相：你活了下來，但秘密永遠埋進了深井。")
        elif choice == "C":
            if self.p.suspicion >= 50:
                self.end("覺醒：你停下了他的自爆，原來他也是曾被遺棄的執法者。")
            else:
                self.p.hp = 0
                self.end("無謂的溫柔：你還沒看透真相，爆炸奪走了一切。")

    def end(self, reason):
        print("\n" + "*"*40)
        print(f"最終結局：{reason}")
        print("*"*40)
        return False

if __name__ == "__main__":
    game = CyberGame()
    game.start()
