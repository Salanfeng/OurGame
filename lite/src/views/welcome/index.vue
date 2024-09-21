<script setup lang="ts">
import { ref } from "vue";
import { ElInput, ElButton, ElMessage } from "element-plus";
import { queryData, modifyData } from "@/api/user";

defineOptions({
  name: "Welcome"
});

const inputText = ref("");
const handleModify = async () => {
  try {
    const response = await modifyData({ value: inputText.value });
    console.log("修改成功:", response);
    ElMessage.success("修改成功");
  } catch (error) {
    console.error("修改失败:", error);
    ElMessage.error("修改失败");
  }
};

const handleQuery = async () => {
  try {
    const response = await queryData({ value: inputText.value });
    console.log("查询结果:", response);
    if (response.success && response.data) {
      inputText.value = response.data.value; // 将查询结果放到文本框中
      console.log(response.data);
      ElMessage.success("查询成功");
    } else {
      ElMessage.error("查询失败");
    }
  } catch (error) {
    console.error("查询失败:", error);
    ElMessage.error("查询失败");
  }
};
</script>

<template>
  <div style="text-align: center">
    <h1>Pure-Admin-Thin（国际化版本）</h1>
    <!-- 添加文本框 -->
    <el-input
      v-model="inputText"
      placeholder="请输入数据"
      style="margin-bottom: 10px"
    />
    <!-- 添加修改按钮 -->
    <el-button style="margin-right: 10px" type="primary" @click="handleModify">
      修改
    </el-button>
    <!-- 添加查询按钮 -->
    <el-button type="primary" @click="handleQuery">查询</el-button>
  </div>
</template>

<style scoped>
/* 添加一些简单的样式 */
h1 {
  margin-bottom: 20px;
}
</style>
