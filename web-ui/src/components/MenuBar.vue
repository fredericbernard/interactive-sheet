<template>
<div style="display: flex; flex-direction: column; justify-content: center;">
  <button class="button" v-on:click="clearDrawing">
    Clear Canvas
  </button>

  <button class="button">
  Clear Canvas
</button>
</div>
</template>

<script>
import {clearDrawing} from '@/api';

export default {
methods: {clearDrawing}
}
</script>

<style>

</style>
