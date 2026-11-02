"""A tiny playable game template for the course demo. No AI is used."""

from html import escape


def build_game(idea: str) -> str:
    title = escape(idea[:80])
    return GAME_HTML.replace("__TITLE__", title)


GAME_HTML = """<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Мини-игра</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:system-ui,sans-serif;color:#fff;background:linear-gradient(135deg,#141451,#7434cc);text-align:center}
main{max-width:560px;margin:auto;padding:24px}h1{font-size:1.5rem}p{line-height:1.5}
#field{height:55vh;min-height:300px;position:relative;border:2px solid #ffffff88;border-radius:20px;background:#ffffff18;overflow:hidden}
#target{position:absolute;width:66px;height:66px;border:0;border-radius:50%;font-size:34px;cursor:pointer;background:#ffd560;box-shadow:0 6px 20px #0005}
#start{padding:12px 24px;border:0;border-radius:12px;background:#fff;color:#4d27a8;font-weight:700;font-size:1rem;cursor:pointer}
.stats{display:flex;justify-content:space-around;font-size:1.2rem;font-weight:700;margin:16px 0}
</style></head><body><main>
<h1>__TITLE__</h1><p>Демо-игра по вашей идее: нажимайте на звезду как можно чаще за 20 секунд.</p>
<div class="stats"><span>Очки: <b id="score">0</b></span><span>Время: <b id="time">20</b></span></div>
<div id="field"><button id="target" hidden aria-label="Поймать звезду">⭐</button></div>
<p id="message">Нажмите «Начать»</p><button id="start">Начать</button>
</main><script>
const field=document.getElementById('field'),target=document.getElementById('target');
const scoreEl=document.getElementById('score'),timeEl=document.getElementById('time');
const message=document.getElementById('message'),start=document.getElementById('start');
let score=0,left=20,timer=null;
function move(){target.style.left=Math.random()*Math.max(0,field.clientWidth-70)+'px';target.style.top=Math.random()*Math.max(0,field.clientHeight-70)+'px'}
target.addEventListener('click',()=>{if(!timer)return;score++;scoreEl.textContent=score;move()});
start.addEventListener('click',()=>{clearInterval(timer);score=0;left=20;scoreEl.textContent=score;timeEl.textContent=left;
target.hidden=false;start.textContent='Начать заново';message.textContent='Ловите звезду!';move();
timer=setInterval(()=>{left--;timeEl.textContent=left;if(left<=0){clearInterval(timer);timer=null;target.hidden=true;message.textContent='Игра окончена! Ваш счёт: '+score}},1000)});
</script></body></html>"""
