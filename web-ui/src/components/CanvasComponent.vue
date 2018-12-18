<template>
<div class="container">
  <canvas ref="canvas" v-bind:width="width" v-bind:height="height"/>
</div>
</template>

<script>
import {
  getDrawing
} from '@/api';

export default {
  data: () => ({
    lines: [{
      "start": [0, 0],
      "end": [100, 100]
    }],
    scalingFactor: 2
  }),
  computed: {
    width: function() {return 216 * this.scalingFactor},
    height: function() {return 279 * this.scalingFactor},
  },
  methods: {
    draw() {
      const ctx = this.$refs.canvas.getContext("2d");

      ctx.clearRect(0, 0, this.$refs.canvas.width * this.scalingFactor,
      this.$refs.canvas.height * this.scalingFactor );

      ctx.beginPath();

      for (let line of this.lines) {
        ctx.moveTo(line.start[0] * this.scalingFactor, line.start[1] * this.scalingFactor);
        ctx.lineTo(line.end[0] * this.scalingFactor, line.end[1] * this.scalingFactor);
        ctx.stroke();
      }
    },
    async update() {
      const drawing = await getDrawing();
      this.lines = drawing.lines;
      this.draw();
    }
  },
  mounted() {
    this.draw();
    setInterval(this.update, 1000);
  }
}
</script>

<style scoped>
canvas {
  border: solid 4px;
  border-color: blue;
}
</style>
