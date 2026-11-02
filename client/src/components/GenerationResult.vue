<script setup>
import { ref } from 'vue'
import { ChevronLeft, MoreVertical, Sparkles } from 'lucide-vue-next'
import skyCover from '../assets/featured-sky-realms.png'

defineProps({
  title: { type: String, default: 'SkyBound' },
  cover: { type: String, default: skyCover },
  tags: { type: Array, default: () => ['Приключения', 'Исследование', 'Полет'] },
  description: { type: String, default: 'Яркий мир парящих островов, где игроки исследуют, строят, развивают свои базы, приручают существ и открывают забытые цивилизации.' },
})
const emit = defineEmits(['back', 'repair', 'moderate'])
const menuOpen = ref(false)
const repairOpen = ref(false)
const repairText = ref('')
const confetti = Array.from({ length: 40 }, (_, index) => ({
  left: index < 10 ? 1 + (index % 2) * 2 : index < 20 ? 96 + (index % 2) * 2 : 6 + ((index * 13) % 88),
  top: index < 20 ? 10 + (index % 10) * 8 : 3 + ((index * 7) % 9),
  rotation: (index * 47) % 180,
  color: ['#a653ff', '#ffbd20', '#27d4e9', '#ff67c7', '#55d55a'][index % 5],
  shape: index % 3,
}))
function repair() {
  if (!repairText.value.trim()) return
  emit('repair', repairText.value.trim())
  repairOpen.value = false
  repairText.value = ''
}
</script>

<template>
  <section class="generation-result">
    <header class="result-header">
      <button class="result-icon" aria-label="Вернуться в лобби" @click="emit('back')"><ChevronLeft :size="22" :stroke-width="1.8" /></button>
      <h1>Игра готова!</h1>
      <div class="result-menu-anchor">
        <button class="result-icon" aria-label="Меню результата" :aria-expanded="menuOpen" @click="menuOpen = !menuOpen"><MoreVertical :size="20" /></button>
        <div v-if="menuOpen" class="result-menu"><button @click="emit('back'); menuOpen = false">Вернуться в лобби</button></div>
      </div>
    </header>

    <div class="result-celebration">
      <div class="result-confetti" aria-hidden="true">
        <i v-for="(piece, index) in confetti" :key="index" :class="`confetti-shape-${piece.shape}`" :style="{ left: `${piece.left}%`, top: `${piece.top}%`, backgroundColor: piece.color, transform: `rotate(${piece.rotation}deg)` }"></i>
      </div>
      <div class="result-cover">
        <img :src="cover" :alt="title" />
        <h2>{{ title }}</h2>
      </div>
      <ul class="result-tags" aria-label="Жанры игры"><li v-for="tag in tags" :key="tag">{{ tag }}</li></ul>
    </div>

    <section class="result-concept" aria-labelledby="concept-title">
      <h3 id="concept-title">Концепция игры</h3>
      <p>{{ description }}</p>
    </section>

    <div class="result-actions">
      <button class="result-repair" @click="repairOpen = !repairOpen"><Sparkles :size="21" :stroke-width="1.8" aria-hidden="true" />Починить с ИИ</button>
      <form v-if="repairOpen" class="repair-form" @submit.prevent="repair">
        <label for="repair-request">Что нужно исправить?</label>
        <textarea id="repair-request" v-model="repairText" placeholder="Опишите проблему или желаемое изменение…" maxlength="1000" required></textarea>
        <div><button type="button" @click="repairOpen = false">Отмена</button><button type="submit">Отправить</button></div>
      </form>
      <button class="result-moderate" @click="emit('moderate')">Отправить на модерацию</button>
    </div>
  </section>
</template>

<style scoped>
.generation-result {
  width: 100%; max-width: 360px; min-height: calc(100dvh - 40px);
  margin: 0 auto; color: #171344; background: white; font-family: Arial, sans-serif;
  text-align: left; line-height: 1.35; letter-spacing: 0;
}
.generation-result *, .generation-result *::before, .generation-result *::after { box-sizing: border-box; }
.generation-result button, .generation-result textarea { font: inherit; }
.result-header { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-bottom: 11px; }
.result-header h1 { flex: 1; margin: 0; font-family: inherit; font-size: 20px; font-weight: 700; line-height: 1.3; text-align: center; color: #171344; letter-spacing: -.4px; }
.result-icon { display: grid; place-items: center; width: 28px; height: 31px; padding: 0; border: 0; background: none; color: #191445; cursor: pointer; }
.result-menu-anchor { position: relative; }
.result-menu { position: absolute; top: 34px; right: 0; z-index: 5; min-width: 165px; padding: 6px; border: 1px solid #ece5f7; border-radius: 10px; background: white; box-shadow: 0 6px 20px #2c19431a; }
.result-menu button { padding: 8px 6px; border: 0; background: none; color: #795f9c; font-size: 11px; cursor: pointer; }
.result-celebration { position: relative; padding: 33px 11px 0; }
.result-confetti { position: absolute; inset: 0 -8px -10px; pointer-events: none; overflow: hidden; }
.result-confetti i { position: absolute; display: block; width: 5px; height: 10px; }
.result-confetti .confetti-shape-1 { width: 5px; height: 5px; }
.result-confetti .confetti-shape-2 { width: 6px; height: 11px; border-radius: 50% 0 50% 0; }
.result-cover { position: relative; aspect-ratio: 1.32; border-radius: 17px; overflow: hidden; background: #d6edff; }
.result-cover img { display: block; width: 100%; height: 100%; object-fit: cover; object-position: 61% center; }
.result-cover::after { position: absolute; inset: 45% 0 0; content: ''; background: linear-gradient(0deg, #263b9399, transparent); pointer-events: none; }
.result-cover h2 { position: absolute; z-index: 1; bottom: 17px; left: 8px; right: 8px; margin: 0; font-family: inherit; font-size: 39px; line-height: 1.05; font-weight: 800; letter-spacing: -1.5px; color: white; text-align: center; overflow-wrap: anywhere; text-shadow: 0 3px 4px #1d36744d; }
.result-tags { display: flex; flex-wrap: wrap; justify-content: center; gap: 6px; padding: 0; margin: 11px 0 14px; list-style: none; }
.result-tags li { padding: 5px 11px; border-radius: 20px; background: #eef3ff; color: #8285d5; font-size: 10px; line-height: 1.2; }
.result-concept { margin: 0 4px; }
.result-concept h3 { margin: 0 0 6px; font-family: inherit; font-size: 16px; font-weight: 700; color: #171344; line-height: 1.2; }
.result-concept p { margin: 0; color: #9991ae; font-size: 13px; line-height: 1.35; }
.result-actions { display: flex; flex-direction: column; gap: 9px; margin-top: 7px; }
.generation-result .result-repair, .generation-result .result-moderate { display: flex; align-items: center; justify-content: center; gap: 12px; width: 100%; min-height: 49px; padding: 10px; border-radius: 13px; font-size: 15px; cursor: pointer; }
.result-repair { border: 1px solid transparent; background: linear-gradient(100deg, #8053ff, #7747ff); color: #fff; font-weight: 700 !important; box-shadow: 0 4px 11px #7f54ff0d; }
.result-moderate { border: 1px solid #9a72ff; background: white; color: #7740ff; }
.repair-form { padding: 12px; border: 1px solid #e9e1f8; border-radius: 12px; }
.repair-form label { display: block; margin-bottom: 8px; color: #675383; font-size: 12px; }
.repair-form textarea { width: 100%; min-height: 85px; padding: 8px; border: 1px solid #e9e1f8; border-radius: 7px; resize: vertical; background: #fbf9ff; color: #332844; font-size: 12px; }
.repair-form > div { display: flex; justify-content: flex-end; gap: 16px; margin-top: 5px; }
.repair-form button { padding: 5px 0; border: 0; background: none; color: #8054bb; font-size: 12px; cursor: pointer; }
.generation-result button:focus-visible, .generation-result textarea:focus-visible { outline: 2px solid #a987ea; outline-offset: 3px; }
@media (max-width: 359px) { .result-cover h2 { font-size: 34px; }.result-tags li { padding: 5px 8px; font-size: 9px; } }
</style>
