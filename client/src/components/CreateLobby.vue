<script setup>
import { computed, ref } from 'vue'
import { ChevronLeft, Search, Plus, UserRound, X, DollarSign } from 'lucide-vue-next'

const props = defineProps({
  users: { type: Array, default: () => [] },
})
const emit = defineEmits(['back', 'create'])
const name = ref('')
const genre = ref('Симуляторы')
const query = ref('')
const selectedUsers = ref([])
const searchInput = ref(null)
const genres = ['Экшен', 'Приключения', 'Головоломки', 'RPG', 'Симуляторы', 'Стратегия', 'Гонки', 'Казуальные']
const matches = computed(() => props.users.filter(user =>
  user.display_name.toLowerCase().includes(query.value.toLowerCase()) &&
  !selectedUsers.value.some(selected => selected.id === user.id),
))

function invite(user) {
  if (selectedUsers.value.length >= 4) return
  selectedUsers.value.push(user)
  query.value = ''
}

function submit() {
  if (!name.value.trim()) return
  emit('create', {
    name: name.value.trim(),
    genre: genre.value,
    participants: selectedUsers.value.map(user => user.id),
  })
}
</script>

<template>
  <section class="create-lobby">
    <header class="create-header">
      <button type="button" class="back-button" aria-label="Назад" @click="emit('back')">
        <ChevronLeft :size="22" :stroke-width="1.8" />
      </button>
      <h1>Создание лобби</h1>
      <span class="header-spacer" aria-hidden="true"></span>
    </header>

    <form class="create-form" @submit.prevent="submit">
      <label class="name-field">
        <span class="field-title">Название лобби</span>
        <input v-model="name" required minlength="2" maxlength="100" placeholder="например, Уютное фермерское приключение" />
      </label>

      <fieldset class="genre-field">
        <legend class="field-title">Жанр игры</legend>
        <div class="genre-grid">
          <button
            v-for="item in genres"
            :key="item"
            type="button"
            class="genre-chip"
            :class="{ 'genre-chip--selected': genre === item }"
            :aria-pressed="genre === item"
            @click="genre = item"
          >{{ item }}</button>
        </div>
      </fieldset>

      <section class="invite-field" aria-labelledby="invite-title">
        <h2 id="invite-title" class="field-title">Пригласить участников</h2>
        <label class="invite-search">
          <Search :size="17" :stroke-width="1.8" aria-hidden="true" />
          <input ref="searchInput" v-model="query" aria-label="Поиск участников" placeholder="Поиск пользователей..." />
        </label>

        <div v-if="query.trim()" class="invite-results">
          <button v-for="user in matches" :key="user.id" type="button" @click="invite(user)">
            {{ user.display_name }}<Plus :size="15" />
          </button>
          <p v-if="!matches.length">Пользователи не найдены</p>
        </div>

        <div class="invited-users">
          <button
            v-for="(user, index) in selectedUsers"
            :key="user.id"
            type="button"
            class="invite-avatar"
            :class="`invite-avatar--${index}`"
            :aria-label="`Убрать участника ${user.display_name}`"
            @click="selectedUsers.splice(index, 1)"
          >
            <img v-if="user.avatar_url" :src="user.avatar_url" :alt="user.display_name" />
            <UserRound v-else :size="22" aria-hidden="true" />
            <X class="remove-user" :size="12" aria-hidden="true" />
          </button>
          <span v-for="slot in 4 - selectedUsers.length" :key="`empty-${slot}`" class="avatar-placeholder" aria-hidden="true">
            <UserRound :size="21" :stroke-width="1.5" />
          </span>
          <button type="button" class="add-user" aria-label="Найти участника" @click="searchInput?.focus()">
            <Plus :size="21" :stroke-width="1.6" />
          </button>
        </div>
      </section>

      <aside class="generation-price">
        <div class="price-row">
          <span class="credit-coin" aria-hidden="true"><DollarSign :size="25" :stroke-width="2.8" /></span>
          <div>
            <p>Стоимость генерации</p>
            <strong>50 кредитов</strong>
          </div>
        </div>
        <p class="price-note">ИИ поможет превратить ваши идеи в играбельную игру.</p>
      </aside>

      <button class="create-button" type="submit">Создать лобби</button>
    </form>
  </section>
</template>

<style scoped>
.create-lobby {
  width: 100%;
  max-width: 360px;
  min-height: calc(100dvh - 40px);
  margin: 0 auto;
  color: #121044;
  font-family: Arial, sans-serif;
  text-align: left;
  line-height: 1.35;
  letter-spacing: 0;
}
.create-lobby *, .create-lobby *::before, .create-lobby *::after { box-sizing: border-box; }
.create-lobby button, .create-lobby input { font: inherit; }
.create-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  min-height: 32px;
}
.create-header h1 {
  margin: 0;
  color: #121044;
  font-family: inherit;
  font-size: 19px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -.4px;
}
.back-button, .header-spacer { width: 25px; flex-shrink: 0; }
.back-button { display: grid; place-items: center; padding: 0; border: 0; background: none; color: #171047; cursor: pointer; }
.create-form { display: flex; flex-direction: column; gap: 20px; }
.name-field { display: flex; flex-direction: column; gap: 7px; }
.field-title { display: block; margin: 0; font-family: inherit; font-size: 14px; font-weight: 700; color: #161342; line-height: 1.3; }
.name-field input {
  width: 100%; height: 42px; padding: 0 13px;
  border: 1px solid #eeedf7; border-radius: 8px;
  background: #f7f7fc; color: #242044; font-size: 11px;
}
.name-field input::placeholder { color: #b3b3ce; }
.genre-field { min-width: 0; margin: 0; padding: 0; border: 0; }
.genre-field legend { margin-bottom: 9px; padding: 0; }
.genre-grid { display: grid; grid-template-columns: repeat(4, auto); gap: 9px 5px; }
.genre-chip {
  padding: 10px 5px; border: 0; border-radius: 18px;
  background: #f3f2fb; color: #7f7ba5; font-size: 11px !important;
  white-space: nowrap; cursor: pointer;
}
.genre-chip--selected {
  background: linear-gradient(105deg, #9570ff, #7246ff);
  color: white; box-shadow: 0 3px 8px #7549ff16;
}
.invite-field { position: relative; margin-top: 5px; }
.invite-search {
  display: flex; align-items: center; gap: 9px;
  margin-top: 9px; padding: 0 12px; height: 38px;
  border-radius: 12px; background: #f0f1f8; color: #29244f;
}
.invite-search svg { flex-shrink: 0; }
.invite-search input { width: 100%; min-width: 0; padding: 0; border: 0; background: none; color: #29244f; font-size: 12px; outline: 0; }
.invite-search input::placeholder { color: #a1a3bf; }
.invited-users { display: flex; align-items: center; justify-content: space-between; gap: 10px; margin-top: 15px; }
.invite-avatar, .avatar-placeholder, .add-user {
  display: grid; place-items: center; position: relative;
  width: 49px; height: 49px; flex-shrink: 0;
  padding: 0; border: 0; border-radius: 50%; background: #f1f0f8; color: #9690b2;
}
.avatar-placeholder { border: 1px dashed #cbc5df; }
.invite-avatar { cursor: pointer; }
.invite-avatar img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
.invite-avatar--0 { background: #d5f0ff; }
.invite-avatar--1 { background: #e7d8ff; }
.invite-avatar--2 { background: #ffddf0; }
.invite-avatar--3 { background: #ffe9c8; }
.remove-user { position: absolute; top: -2px; right: -2px; border-radius: 50%; background: #fff; color: #6c5d92; }
.add-user { color: #39335f; cursor: pointer; }
.invite-results { margin-top: 6px; border: 1px solid #ece8f6; border-radius: 10px; padding: 6px; }
.invite-results button { display: flex; align-items: center; justify-content: space-between; width: 100%; border: 0; padding: 8px; background: white; color: #29244f; cursor: pointer; font-size: 12px; }
.invite-results p { margin: 5px; font-size: 11px; color: #89819f; }
.generation-price { margin-top: 0; padding: 16px 12px 13px; border-radius: 13px; background: linear-gradient(110deg, #f1eaff, #ece4ff); }
.price-row { display: flex; align-items: center; justify-content: center; gap: 13px; }
.price-row p { margin: 0 0 3px; color: #6330eb; font-size: 12px; }
.price-row strong { display: block; color: #6128f5; font-size: 22px; font-weight: 700; line-height: 1.15; }
.credit-coin {
  display: grid; place-items: center; width: 47px; height: 47px;
  border-radius: 50%; border: 4px solid #ffe19b;
  background: linear-gradient(135deg, #ffca43, #ff9c22); color: #fff7d1;
  box-shadow: 0 3px 5px #d99a4729, inset 0 0 0 2px #efaa32;
}
.price-note { margin: 13px 0 0; text-align: center; color: #9d7ddd; font-size: 10px; line-height: 1.45; }
.create-lobby .create-button {
  width: 100%; height: 47px; margin-top: -8px; padding: 0 12px;
  border: 0; border-radius: 13px;
  background: linear-gradient(100deg, #7950ff, #7547ff);
  color: #fff; font-size: 16px; font-weight: 700; cursor: pointer;
  box-shadow: 0 4px 10px #7444ff0e;
}
.create-lobby button:focus-visible, .name-field input:focus-visible { outline: 2px solid #ac8aff; outline-offset: 3px; }
.invite-search:focus-within { outline: 2px solid #ac8aff; outline-offset: 2px; }
@media (max-width: 359px) {
  .invite-avatar, .avatar-placeholder, .add-user { width: 40px; height: 40px; }
  .genre-chip { font-size: 10px !important; }
}
</style>
