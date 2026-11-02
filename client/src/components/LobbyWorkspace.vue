<script setup>
import { computed, ref } from 'vue'
import { ChevronLeft, MoreVertical, UserRound, ThumbsUp, Check, X, Clock3, Plus, Send } from 'lucide-vue-next'

defineProps({ name: { type: String, default: 'Fantasy RPG World' } })
const emit = defineEmits(['back', 'generate'])
const activeTab = ref('ideas')
const openMenu = ref(null)
const showComposer = ref(false)
const ideaText = ref('')
const messageText = ref('')
const messages = ref([])
// Примеры из макета. Позже заменим списком идей из API.
const ideas = ref([
  { id: 1, body: 'Мир с парящими островами', author: 'Alex', age: '2 ч. назад', status: 'accepted', likes: 12, color: 'blue', voted: false },
  { id: 2, body: 'Приручение и езда на существах', author: 'Mira', age: '3 ч. назад', status: 'rejected', likes: 4, color: 'pink', voted: false },
  { id: 3, body: 'Динамическая погода и сезоны', author: 'You', age: '4 ч. назад', status: 'accepted', likes: 8, color: 'gold', voted: false },
  { id: 4, body: 'Дирижабли игрока', author: 'Ken', age: '5 ч. назад', status: 'proposed', likes: 6, color: 'green', voted: false },
])
const requiredIdeas = 5
const accepted = computed(() => ideas.value.filter(idea => idea.status === 'accepted').length)
const remaining = computed(() => Math.max(0, requiredIdeas - accepted.value))
const steps = ['Идеи', 'Доработка', 'Генерация', 'Результат']
const statuses = {
  accepted: { label: 'Принято', icon: Check },
  rejected: { label: 'Отклонено', icon: X },
  proposed: { label: 'На рассмотрении', icon: Clock3 },
}

function changeStatus(idea, status) {
  idea.status = status
  openMenu.value = null
}
function vote(idea) {
  idea.voted = !idea.voted
  idea.likes += idea.voted ? 1 : -1
}
function addIdea() {
  if (!ideaText.value.trim()) return
  ideas.value.push({ id: Date.now(), body: ideaText.value.trim(), author: 'You', age: 'только что', status: 'proposed', likes: 0, color: 'gold', voted: false })
  ideaText.value = ''
  showComposer.value = false
}
function sendMessage() {
  if (!messageText.value.trim()) return
  messages.value.push({ id: Date.now(), text: messageText.value.trim() })
  messageText.value = ''
}
</script>

<template>
  <section class="workspace">
    <header class="workspace-header">
      <button class="workspace-icon" aria-label="Назад" @click="emit('back')"><ChevronLeft :size="22" /></button>
      <div class="workspace-heading">
        <h1>{{ name }}</h1>
        <p>{{ accepted }}/{{ requiredIdeas }} идей принято</p>
      </div>
      <div class="workspace-menu-anchor">
        <button class="workspace-icon" aria-label="Меню лобби" :aria-expanded="openMenu === 'lobby'" @click="openMenu = openMenu === 'lobby' ? null : 'lobby'"><MoreVertical :size="20" /></button>
        <div v-if="openMenu === 'lobby'" class="workspace-dropdown">
          <button @click="showComposer = true; activeTab = 'ideas'; openMenu = null"><Plus :size="15" />Добавить идею</button>
        </div>
      </div>
    </header>

    <div class="workspace-members" aria-label="Участники лобби: заглушки аватаров">
      <span v-for="color in ['blue', 'green', 'cyan', 'purple']" :key="color" class="member-avatar" :class="`avatar-${color}`"><UserRound :size="24" :stroke-width="1.5" /></span>
      <span class="members-more">+2</span>
    </div>

    <ol class="workspace-steps" aria-label="Этапы создания игры">
      <li v-for="(step, index) in steps" :key="step" :class="{ 'step-active': index === 0 }" :aria-current="index === 0 ? 'step' : undefined">
        <span class="step-number">{{ index + 1 }}</span>
        <span class="step-label">{{ step }}</span>
      </li>
    </ol>

    <div class="workspace-tabs" role="tablist" aria-label="Разделы лобби">
      <button id="ideas-tab" role="tab" :aria-selected="activeTab === 'ideas'" aria-controls="ideas-panel" :class="{ selected: activeTab === 'ideas' }" @click="activeTab = 'ideas'">Идеи</button>
      <button id="discussion-tab" role="tab" :aria-selected="activeTab === 'discussion'" aria-controls="discussion-panel" :class="{ selected: activeTab === 'discussion' }" @click="activeTab = 'discussion'">Обсуждение</button>
    </div>

    <section v-if="activeTab === 'ideas'" id="ideas-panel" role="tabpanel" aria-labelledby="ideas-tab">
      <form v-if="showComposer" class="idea-composer" @submit.prevent="addIdea">
        <textarea v-model="ideaText" aria-label="Новая идея" placeholder="Опишите идею для игры…" required maxlength="500"></textarea>
        <div><button type="button" @click="showComposer = false">Отмена</button><button type="submit">Добавить идею</button></div>
      </form>

      <div class="idea-list">
        <article v-for="idea in ideas" :key="idea.id" class="idea-card">
          <span class="idea-avatar" :class="`avatar-${idea.color}`" aria-hidden="true"><UserRound :size="22" :stroke-width="1.5" /></span>
          <div class="idea-content">
            <h2>{{ idea.body }}</h2>
            <div class="idea-meta">
              <span>{{ idea.author }}</span><span>{{ idea.age }}</span>
              <span class="idea-status" :class="`status-${idea.status}`"><component :is="statuses[idea.status].icon" :size="10" />{{ statuses[idea.status].label }}</span>
            </div>
          </div>
          <div class="idea-actions">
            <button class="idea-more" aria-label="Изменить статус идеи" :aria-expanded="openMenu === idea.id" @click="openMenu = openMenu === idea.id ? null : idea.id"><MoreVertical :size="15" /></button>
            <button class="idea-vote" :class="{ voted: idea.voted }" :aria-pressed="idea.voted" :aria-label="`Поддержать идею: ${idea.body}`" @click="vote(idea)"><ThumbsUp :size="13" />{{ idea.likes }}</button>
          </div>
          <div v-if="openMenu === idea.id" class="workspace-dropdown idea-dropdown">
            <button v-for="(status, key) in statuses" :key="key" @click="changeStatus(idea, key)"><component :is="status.icon" :size="14" />{{ status.label }}</button>
          </div>
        </article>
      </div>

      <button class="generate-button" :disabled="remaining > 0" @click="emit('generate')">Сгенерировать игру</button>
      <p class="generation-hint">{{ remaining ? `Нужно ещё ${remaining} принятых идей` : 'Все идеи приняты — можно создавать игру' }}</p>
    </section>

    <section v-else id="discussion-panel" class="discussion-panel" role="tabpanel" aria-labelledby="discussion-tab">
      <p v-if="!messages.length" class="discussion-empty">Обсудите идеи с участниками лобби</p>
      <article v-for="message in messages" :key="message.id" class="discussion-message"><strong>Вы</strong><p>{{ message.text }}</p></article>
      <form class="discussion-compose" @submit.prevent="sendMessage"><input v-model="messageText" aria-label="Сообщение" placeholder="Написать сообщение…" maxlength="1000" required /><button aria-label="Отправить сообщение"><Send :size="18" /></button></form>
    </section>
  </section>
</template>

<style scoped>
.workspace { width: 100%; max-width: 360px; margin: 0 auto; color: #171344; font-family: Arial, sans-serif; font-size: 13px; line-height: 1.35; letter-spacing: 0; text-align: left; }
.workspace *, .workspace *::before, .workspace *::after { box-sizing: border-box; }
.workspace button, .workspace input, .workspace textarea { font: inherit; }
.workspace button { cursor: pointer; }
.workspace-header { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 20px; }
.workspace-icon { display: grid; place-items: center; width: 27px; height: 29px; padding: 0; background: none; border: 0; color: #191445; }
.workspace-heading { flex: 1; min-width: 0; text-align: center; }
.workspace-heading h1 { margin: 0; font-family: inherit; font-size: 19px; font-weight: 700; line-height: 1.3; color: #171344; letter-spacing: -.4px; overflow-wrap: anywhere; }
.workspace-heading p { margin: 1px 0 0; font-size: 12px; color: #a19bb9; }
.workspace-menu-anchor { position: relative; }
.workspace-members { display: flex; justify-content: center; align-items: center; gap: 8px; margin-bottom: 18px; }
.member-avatar, .members-more, .idea-avatar { display: grid; place-items: center; flex-shrink: 0; border-radius: 50%; }
.member-avatar { width: 40px; height: 40px; border: 2px solid white; box-shadow: 0 0 0 1px #ede8f6; }
.members-more { width: 40px; height: 40px; background: #f1f0f9; color: #27204d; font-size: 14px; }
.avatar-blue { background: #d9effe; color: #4988bb; }
.avatar-green { background: #dcebdd; color: #659577; }
.avatar-cyan { background: #d5eff3; color: #428ea3; }
.avatar-purple { background: #eedbff; color: #9a5ac0; }
.avatar-pink { background: #fbe0ef; color: #b57b9a; }
.avatar-gold { background: #ffebd2; color: #b98d52; }
.workspace-steps { display: flex; list-style: none; padding: 0; margin: 0 0 17px; }
.workspace-steps li { position: relative; flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px; color: #a19cb8; }
.workspace-steps li:not(:last-child)::after { content: ''; position: absolute; top: 15px; left: calc(50% + 21px); width: calc(100% - 42px); height: 2px; background: #efedf6; }
.workspace-steps li.step-active::after { background: #a684ff; }
.step-number { display: grid; place-items: center; width: 31px; height: 31px; border-radius: 50%; background: #ebeaf3; color: #6f6a97; font-size: 16px; }
.step-label { font-size: 11px; }
.step-active .step-number { background: linear-gradient(140deg, #ab83ff, #7445ff); color: white; box-shadow: 0 3px 8px #8255ff20; }
.step-active .step-label { color: #8b55ff; }
.workspace-tabs { display: flex; background: #f3f0fd; border-radius: 24px; margin-bottom: 13px; padding: 0; }
.workspace-tabs button { flex: 1; padding: 9px 5px; border: 0; border-radius: 24px; background: none; color: #9990b6; font-size: 12px; }
.workspace-tabs button.selected { color: white; background: linear-gradient(100deg, #9365ff, #7747ff); box-shadow: 0 3px 8px #7a50fa14; }
.idea-list { display: flex; flex-direction: column; gap: 9px; }
.idea-card { display: flex; align-items: center; position: relative; gap: 9px; min-height: 65px; padding: 10px 8px; border: 1px solid #eceaf4; border-radius: 11px; background: #fff; box-shadow: 0 2px 5px #7d6eae04; }
.idea-avatar { width: 36px; height: 36px; }
.idea-content { flex: 1; min-width: 0; }
.idea-content h2 { margin: 0 0 6px; font-family: inherit; font-size: 12px; font-weight: 500; color: #25204f; letter-spacing: -.15px; line-height: 1.35; overflow-wrap: anywhere; }
.idea-meta { display: flex; align-items: center; gap: 7px; flex-wrap: wrap; font-size: 10px; color: #9992af; }
.idea-meta > span:nth-child(2) { color: #b0a7bf; font-size: 9px; }
.idea-status { display: inline-flex; align-items: center; gap: 2px; padding: 3px 6px; border-radius: 8px; font-size: 9px; line-height: 1; white-space: nowrap; }
.status-accepted { color: #23a77d; background: #d9f8ed; }
.status-rejected { color: #f16885; background: #ffe5eb; }
.status-proposed { color: #9e94b5; background: #f2eff8; }
.idea-actions { align-self: stretch; display: flex; flex-direction: column; align-items: flex-end; justify-content: space-between; gap: 4px; }
.idea-more { display: grid; place-items: center; width: 20px; height: 18px; border: 0; padding: 0; background: none; color: #7970a4; }
.idea-vote { display: flex; align-items: center; gap: 4px; padding: 0; border: 0; background: none; color: #9a90b7; font-size: 10px !important; }
.idea-vote.voted { color: #794bff; }
.workspace-dropdown { position: absolute; right: 0; top: 32px; z-index: 5; padding: 5px; min-width: 155px; border: 1px solid #e9e3f7; border-radius: 10px; background: white; box-shadow: 0 7px 25px #29203e18; }
.workspace-dropdown button { display: flex; align-items: center; gap: 7px; width: 100%; padding: 9px 7px; border: 0; background: none; color: #6d5b94; text-align: left; font-size: 11px; }
.workspace-dropdown button:hover { background: #f8f5ff; border-radius: 6px; }
.idea-dropdown { top: 29px; right: 8px; }
.workspace .generate-button { width: 100%; margin-top: 15px; padding: 15px 8px; border: 0; border-radius: 13px; background: linear-gradient(100deg, #9664ff, #7445ff); color: white; font-size: 15px; font-weight: 700; }
.workspace .generate-button:disabled { background: linear-gradient(100deg, #c8b3ff, #bfa5ff); cursor: default; }
.generation-hint { margin: 5px 0 0; color: #a59ab9; font-size: 11px; text-align: center; }
.idea-composer { padding: 11px; border: 1px solid #e9e2f5; border-radius: 11px; margin-bottom: 10px; }
.idea-composer textarea { width: 100%; min-height: 75px; resize: vertical; padding: 8px; background: #faf8ff; border: 1px solid #eee8fa; border-radius: 7px; color: #31284e; font-size: 12px; }
.idea-composer > div { display: flex; justify-content: flex-end; gap: 12px; margin-top: 6px; }
.idea-composer button { padding: 6px 0; border: 0; background: none; color: #8053d7; font-size: 11px; }
.discussion-panel { min-height: 250px; }
.discussion-empty { margin: 35px 10px; color: #a49bb8; font-size: 12px; text-align: center; }
.discussion-message { margin: 10px 0; padding: 12px; background: #f6f1ff; border-radius: 12px; overflow-wrap: anywhere; }
.discussion-message strong { font-size: 11px; color: #8153c7; }
.discussion-message p { margin: 5px 0 0; font-size: 12px; }
.discussion-compose { display: flex; gap: 8px; padding: 9px; border: 1px solid #e9e3f6; border-radius: 12px; }
.discussion-compose input { flex: 1; min-width: 0; border: 0; padding: 5px; font-size: 12px; background: none; color: #31284e; }
.discussion-compose button { display: grid; place-items: center; border: 0; padding: 5px; border-radius: 7px; background: #8555ff; color: white; }
.workspace button:focus-visible, .workspace input:focus-visible, .workspace textarea:focus-visible { outline: 2px solid #b192f6; outline-offset: 2px; }
@media (max-width: 359px) { .idea-meta { gap: 4px; }.idea-card { padding: 8px 5px; gap: 6px; }.idea-avatar { width: 29px; height: 29px; }.idea-content h2 { font-size: 11px; }.step-label { font-size: 10px; } }
</style>
