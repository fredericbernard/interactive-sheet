<template>
  <div id="app">
    <MainPage />
  </div>
</template>

<script>
import MainPage from '@/components/MainPage.vue';

export default {
  name: 'app',
  components: {
    MainPage
  }
}
</script>

<style lang="scss">
    @import '~bulma/bulma.sass'
</style>
