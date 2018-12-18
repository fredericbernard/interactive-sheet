<template>
<div class="container">
  <CanvasComponent />
  <MenuBar />
</div>
</template>

<script>
import CanvasComponent from '@/components/CanvasComponent'
import MenuBar from '@/components/MenuBar';

export default {
  components: {
    CanvasComponent,
    MenuBar
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  padding-right: 10rem;
  padding-left: 10rem;
  padding-top: 1rem;
}
</style>
