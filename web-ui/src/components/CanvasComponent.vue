<template>
<div class="container">
  <canvas ref="canvas" v-bind:width="width" v-bind:height="height" v-on:mousedown="down" v-on:mousemove="mousemove" v-on:mouseup="up"/>
</div>
</template>

<script>
import {
  getDrawing,
  addLine
} from '@/api';

export default {
  data: () => ({
    lines: [{
      "start": [0, 0],
      "end": [100, 100]
    }],
    scalingFactor: 2,
    lineStart: undefined,
  }),
  computed: {
    width: function() {
      return 216 * this.scalingFactor
    },
    height: function() {
      return 279 * this.scalingFactor
    },
  },
  methods: {
    draw() {
      const ctx = this.$refs.canvas.getContext("2d");

      ctx.clearRect(0, 0, this.$refs.canvas.width * this.scalingFactor,
        this.$refs.canvas.height * this.scalingFactor);

      ctx.beginPath();

      for (let line of this.lines) {
        ctx.moveTo(line.start[0] * this.scalingFactor, line.start[1] * this.scalingFactor);
        ctx.lineTo(line.end[0] * this.scalingFactor, line.end[1] * this.scalingFactor);
        ctx.stroke();
      }

    },
    down(e) {
      const rect = e.target.getBoundingClientRect();
      const x = e.clientX - rect.left; //x position within the element.
      const y = e.clientY - rect.top; //y position within the element.

      this.lineStart = [x / this.scalingFactor, y / this.scalingFactor];
    },
    mousemove(e) {
      if (this.lineStart !== undefined) {
        console.log("move");
      }
    },
    async up(e) {
      const rect = e.target.getBoundingClientRect();
      const x = e.clientX - rect.left; //x position within the element.
      const y = e.clientY - rect.top; //y position within the element.

      addLine(Math.round(this.lineStart[0]), Math.round(this.lineStart[1]), Math.round(x / this.scalingFactor), Math.round(y / this.scalingFactor));
      this.lineStart = undefined;
      console.log("up");
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
