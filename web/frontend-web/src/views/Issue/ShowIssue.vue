<template>
  <div class="showIssue-page">
    <div class="head">Issues</div>
    <main class="fx">
      <div class="left">
        <div class="title">Title: A New Page For Issues</div>
        <section>
          <section-part height="759px" :showList="true"></section-part>
          <section-part></section-part>
          <section-part>
            <div class="tool-bar">
              <!-- 五角星 -->
              <!-- <img src="@/assets/img/star.png" alt="" /> -->
              <!-- 圆圈 -->
              <!-- <img src="@/assets/img/ellipse.png" alt="" /> -->
              <!-- 三角形 -->
              <!-- <img src="@/assets/img/polygon.png" alt="" /> -->
            </div>
            <textarea
              class="textarea"
              cols="30"
              rows="10"
              placeholder="Leave a comment"
            ></textarea>
            <a class="comment fx-c">Comment</a>
          </section-part>
        </section>
      </div>
      <aside>
        <h2>Label</h2>
        <div class="label-list">
          <div class="label-item" v-for="labelItem in 6" :key="labelItem"></div>
        </div>
      </aside>
    </main>
  </div>
</template>

<script>
import SectionPart from "../../components/Issue/SectionPart.vue";
export default {
  components: {
    SectionPart,
  },
};
</script>

<style scoped>
.head {
  height: 69px;
  line-height: 69px;
  text-align: center;
  background: #0077ff;
  font-weight: 500;
  font-size: 40px;
  color: #ffffff;
}

main {
  padding: 18px 43px 0 69px;
}

main .left {
  margin-right: 61px;
}

main .left .title {
  width: 1007px;
  height: 115px;
  line-height: 115px;
  background: #ebeff4;
  font-style: italic;
  font-weight: 600;
  font-size: 40px;
}

main .left section {
  margin-top: 26px;
}

main aside {
  width: 260px;
  height: 894px;
  background: #ebeff4;
  padding: 39px 0 0 32px;
}

main aside h2 {
  font-weight: bold;
  font-size: 24px;
  line-height: 29px;
}

main aside .label-list {
  display: grid;
  grid-template-rows: repeat(2, 1fr);
  grid-template-columns: repeat(3, 1fr);
  grid-row-gap: 9px;
  margin-top: 12px;
}

main aside .label-list .label-item {
  width: 60px;
  height: 36px;
  background: rgba(43, 200, 64, 0.5);
  border-radius: 12px;
}

.tool-bar {
  height: 55px;
  line-height: 55px;
  margin-bottom: 6px;
}

.tool-bar img {
  margin-right: 15px;
}

.textarea {
  width: 855px;
  height: 92px;
  outline: none;
  background: #ebeff4;
  border: 3px solid #0077ff;
  margin-bottom: 13px;
  resize: none;
  font-size: 35px;
  text-indent: 31px;
}

.textarea::-webkit-input-placeholder {
  color: #a3b6cc;
  font-weight: 500;
  font-size: 35px;
  line-height: 42px;
}

.comment {
  width: 160px;
  height: 50px;
  float: right;
  margin-right: 11px;
  background: rgba(43, 200, 64, 0.8);
  border-radius: 15px;
  font-weight: 500;
  font-size: 24px;
  color: #ffffff;
  margin-bottom: 14px;
}
</style>