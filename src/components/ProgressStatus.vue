<template>
  <div class="radial-progress" v-bind:data-progress="progress">
    <!-- //refatorar essa parada do isPaused -->
    <div class="circle" v-bind:style="{ backgroundColor: 'red' }">
      <div class="mask full">
        <div class="fill" :class="{ green : (!state.paused && !state.finished), yellow: state.paused && !state.finished}" ></div>
        
      </div>
      <div class="mask half" >
        <div class="fill " :class="{ green : (!state.paused && !state.finished), yellow: state.paused && !state.finished}"  ></div>
        <div class="fill fix" :class="{ green : (!state.paused && !state.finished), yellow: state.paused && !state.finished}" ></div>
      </div>
      <div class="shadow"></div>
    </div>
    <div class="inset">
      <div class="data">        
        <span class="img"
          ><img
            :src="
              require('../assets/img/' +
                operation.name +
                '-' +
                operation.type +
                '.png')
            "
        /></span>
        <h2>{{ operation.name }} - {{ operation.type }}</h2>
        <h1>{{ insertZero(minutes) }}:{{ insertZero(seconds) }}</h1>
        <h3>{{ operation.placed }}/{{ operation.total }}</h3>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";

export default {
  name: "ProgressStatus",
  computed: {
    ...mapGetters(["operation", "minutes", "seconds", "progress", "state"]),
    ...mapState(["operation"]),
  },

  // watch: {
  //   "$store.state.localTimer.currentSeconds": function () {
  //     console.log("mudoo " + this.$store.state.localTimer.currentSeconds + " minute: " + this.minutes + " seconds: " + this.seconds);
  //   },
  // },
  methods: {
    changeCircleColor() {

    },

    insertZero(n) {
      return n > 9 ? "" + n : "0" + n;
    },
  },

  mounted() {},
};
</script>

<style scoped lang="less">
.radial-progress {
  @circle-background: #ccc; // light-grey
  @circle-color: #27ae60;
  @circle-paused-color: #ffd000;

  @circle-size: 450px;

  @first-color: #0d1d2d;
  @second-color: #fb8c00;

  @transition-length: 1s;
  @transition-type: ease-out;

  @inset-size: 400px;
  @inset-color: #fff; // white
  @shadow: 6px 6px 10px rgba(0, 0, 0, 0.2);

  @percentage-font-size: 22px;
  @percentage-text-width: 44px;

  height: @circle-size;
  width: @circle-size;
  border-radius: 50%;
  top: 50%;
  left: 50%;
  display: flex;

  margin-top: 4em;
  .circle {
    .mask,
    .fill,
    .shadow {
      width: @circle-size;
      height: @circle-size;
      position: absolute;
      border-radius: 50%;
    }
    .shadow {
      box-shadow: @shadow inset;
    }
    .mask,
    .fill {
      -webkit-backface-visibility: hidden;
      transition: transform @transition-length @transition-type;
    }
    .mask {
      clip: rect(0px, @circle-size, @circle-size, @circle-size / 2);

      .fill{
        clip: rect(0px, @circle-size / 2, @circle-size, 0px);
      }

      .green{
        background-color: @circle-color;
      }

      .yellow{
        background-color: @circle-paused-color;
      }
    }
  }

  .inset {
    width: @inset-size;
    height: @inset-size;
    position: absolute;
    margin-left: (@circle-size - @inset-size)/2;
    margin-top: (@circle-size - @inset-size)/2;
    background-color: @inset-color;
    border-radius: 50%;
    box-shadow: @shadow;

    .data {
      text-align: center;
      color: @first-color;

      .img {
        padding: 20px;
        height: 11em;
        display: block;

        img {
          padding: 20px;
          height: 10em;
        }
      }

      h1 {
        font-size: 6rem;
        margin: 0;
        margin-top: -0.2em;
      }
      h2 {
        font-size: 2em;
        margin: 0;
        font-weight: 400;
      }
      h3 {
        color: @second-color;
        font-size: 2em;
        margin: 0;
        margin-top: -0.7em;
      }
    }
  }

  @increment: 180deg / 100;
  @i: 0;
  .loop (@i) when (@i <= 100) {
    &[data-progress="@{i}"] {
      .circle {
        .mask.full,
        .fill {
          transform: rotate(@increment * @i);

          //   &[isPaused="true"] {
          //   background-color: #ffd000;
          // }

          // &[isPaused="false"] {
          //   background-color: #27ae60;
          // }
        }
        .fill.fix {
          transform: rotate(@increment * @i * 2);
        }
        // .fix{

        //   &[isPaused="true"] {
        //   background-color: #ffd000;
        // }

        // &[isPaused="false"] {
        //   background-color: #27ae60;
        // }
        // }
      }
      // .inset .percentage:before {
      //   content: "@{i}%";
      // }
    }
    .loop(@i + 1);
  }
  .loop(@i);
}
</style>
