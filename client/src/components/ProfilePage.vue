<script setup>
import { UserRound, BookOpen, Bookmark, WalletCards, Bell, Settings, ChevronRight } from 'lucide-vue-next'

// Данные для оформления макета. Профиль подключим к API отдельно.
defineProps({
  name: { type: String, default: 'PixelForge' },
  avatar: { type: String, default: '' },
  stats: {
    type: Array,
    default: () => [
      { label: 'Игр', value: '12' },
      { label: 'Лобби', value: '48' },
      { label: 'Подписчиков', value: '2.4K' },
      { label: 'Подписок', value: '320' },
    ],
  },
})
const emit = defineEmits(['open'])
const menu = [
  { id: 'games', label: 'Мои игры', icon: BookOpen, color: 'green' },
  { id: 'saved-lobbies', label: 'Сохранённые лобби', icon: Bookmark, color: 'purple' },
  { id: 'wallet', label: 'Кошелёк / Кредиты', icon: WalletCards, color: 'violet' },
  { id: 'notifications', label: 'Уведомления', icon: Bell, color: 'red' },
  { id: 'settings', label: 'Настройки', icon: Settings, color: 'slate' },
]
</script>

<template>
  <section class="profile-page">
    <header class="profile-identity">
      <div class="profile-avatar">
        <img v-if="avatar" :src="avatar" :alt="name" />
        <UserRound v-else :size="55" :stroke-width="1.4" aria-label="Аватар не добавлен" />
      </div>
      <div class="profile-name">
        <h1>{{ name }}</h1>
        <span class="creator-badge">Создатель игр</span>
      </div>
    </header>

    <dl class="profile-stats">
      <div v-for="stat in stats" :key="stat.label" class="profile-stat">
        <dt>{{ stat.label }}</dt>
        <dd>{{ stat.value }}</dd>
      </div>
    </dl>

    <nav class="profile-menu" aria-label="Меню профиля">
      <button v-for="item in menu" :key="item.id" type="button" @click="emit('open', item.id)">
        <span class="profile-menu-icon" :class="`icon-${item.color}`"><component :is="item.icon" :size="19" :stroke-width="2" aria-hidden="true" /></span>
        <span class="profile-menu-label">{{ item.label }}</span>
        <ChevronRight class="profile-chevron" :size="17" :stroke-width="1.6" aria-hidden="true" />
      </button>
    </nav>
  </section>
</template>

<style scoped>
.profile-page {
  position: relative;
  isolation: isolate;
  width: 100%;
  max-width: 400px;
  min-height: calc(100dvh - 70px);
  margin: 0 auto;
  padding: 38px 16px 24px;
  overflow: hidden;
  color: #171344;
  background: radial-gradient(ellipse at 85% 0%, #c7a7f9 0%, transparent 31%), linear-gradient(180deg, #d9c2ff 0, #f5ebff 120px, #fff 225px);
  font-family: Arial, sans-serif;
  font-size: 14px;
  line-height: 1.35;
  letter-spacing: 0;
  text-align: left;
}
.profile-page *, .profile-page *::before, .profile-page *::after { box-sizing: border-box; }
.profile-page::before {
  content: '';
  position: absolute;
  z-index: -1;
  width: 105px;
  height: 105px;
  top: 6px;
  left: -27px;
  border-radius: 50%;
  background: #e9d4ff66;
}
.profile-page::after {
  content: '';
  position: absolute;
  z-index: -1;
  top: 83px;
  right: 24px;
  width: 29px;
  height: 48px;
  border-radius: 70% 35% 60% 40%;
  background: #dcb6f54d;
  transform: rotate(24deg);
}
.profile-identity { display: flex; align-items: center; gap: 17px; padding: 2px 16px 18px; }
.profile-avatar {
  display: grid;
  place-items: center;
  flex-shrink: 0;
  width: 94px;
  height: 94px;
  border: 4px solid #fff;
  border-radius: 50%;
  color: #8e78ba;
  background: linear-gradient(145deg, #ddedff, #c3b4f8);
  box-shadow: 0 6px 18px #9c71bf12;
  overflow: hidden;
}
.profile-avatar img { display: block; width: 100%; height: 100%; object-fit: cover; }
.profile-name { min-width: 0; }
.profile-name h1 { margin: 0 0 7px; color: #15113e; font-family: inherit; font-size: 23px; font-weight: 700; line-height: 1.2; letter-spacing: -.6px; overflow-wrap: anywhere; }
.creator-badge { display: inline-block; padding: 5px 12px; border-radius: 20px; background: #ffe8ad; color: #5c4029; font-size: 11px; font-weight: 700; white-space: nowrap; }
.profile-stats { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); margin: 0 0 12px; padding: 13px 0; background: #ffffffd9; border: 1px solid #f4effa; border-radius: 13px; box-shadow: 0 3px 10px #9f84c303; }
.profile-stat { display: flex; flex-direction: column-reverse; align-items: center; gap: 4px; min-width: 0; }
.profile-stat + .profile-stat { border-left: 1px solid #eeebf6; }
.profile-stat dt { color: #a19aba; font-size: 10px; font-weight: 400; }
.profile-stat dd { margin: 0; color: #25204f; font-size: 16px; font-weight: 700; line-height: 1.1; }
.profile-menu { padding: 0 7px; border: 1px solid #f5f2fa; border-radius: 13px; background: #ffffffed; }
.profile-menu button { display: flex; align-items: center; gap: 14px; width: 100%; min-height: 49px; padding: 9px 0; border: 0; background: none; text-align: left; font: inherit; color: #49406a; cursor: pointer; }
.profile-menu button + button { border-top: 1px solid #f1eef7; }
.profile-menu-icon { display: grid; place-items: center; flex-shrink: 0; width: 31px; height: 31px; border-radius: 10px; color: white; }
.icon-green { background: linear-gradient(135deg, #57d46e, #22b34b); }
.icon-purple { background: linear-gradient(135deg, #c174ff, #a141ee); }
.icon-violet { background: linear-gradient(135deg, #9479ff, #6d4ff0); }
.icon-red { background: linear-gradient(135deg, #ff6269, #f51e35); }
.icon-slate { background: linear-gradient(135deg, #969fbd, #6b7498); }
.profile-menu-label { flex: 1; font-size: 13px; }
.profile-chevron { flex-shrink: 0; color: #a39ac0; }
.profile-menu button:focus-visible { outline: 2px solid #a68ae6; outline-offset: 2px; border-radius: 8px; }
.profile-menu button:hover { background: #fbf9ff; }
@media (max-width: 359px) {
  .profile-identity { padding-left: 11px; padding-right: 11px; gap: 13px; }
  .profile-avatar { width: 80px; height: 80px; }
  .profile-name h1 { font-size: 21px; }
  .profile-stat dt { font-size: 9px; }
}
</style>
