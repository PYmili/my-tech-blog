<template>
  <!-- 流量统计面板 -->
  <div class="statistics-panel">
    <!-- 面板标题 -->
    <div class="panel-header">
      <h2>流量统计</h2>
      <p>分析您的博客访问数据</p>
    </div>

    <!-- 统计概览卡片 -->
    <el-row :gutter="20" class="overview-row">
      <!-- 今日访问 -->
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="overview-card">
          <el-statistic title="今日访问" :value="statistics.todayViews">
            <template #prefix>
              <el-icon color="#409EFF"><View /></el-icon>
            </template>
          </el-statistic>
          <div class="trend">
            <span :class="statistics.todayTrend >= 0 ? 'up' : 'down'">
              {{ statistics.todayTrend >= 0 ? '↑' : '↓' }}
              {{ Math.abs(statistics.todayTrend) }}%
            </span>
            <span class="label">较昨日</span>
          </div>
        </el-card>
      </el-col>

      <!-- 本周访问 -->
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="overview-card">
          <el-statistic title="本周访问" :value="statistics.weekViews">
            <template #prefix>
              <el-icon color="#67C23A"><TrendCharts /></el-icon>
            </template>
          </el-statistic>
          <div class="trend">
            <span :class="statistics.weekTrend >= 0 ? 'up' : 'down'">
              {{ statistics.weekTrend >= 0 ? '↑' : '↓' }}
              {{ Math.abs(statistics.weekTrend) }}%
            </span>
            <span class="label">较上周</span>
          </div>
        </el-card>
      </el-col>

      <!-- 本月访问 -->
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="overview-card">
          <el-statistic title="本月访问" :value="statistics.monthViews">
            <template #prefix>
              <el-icon color="#E6A23C"><DataAnalysis /></el-icon>
            </template>
          </el-statistic>
          <div class="trend">
            <span :class="statistics.monthTrend >= 0 ? 'up' : 'down'">
              {{ statistics.monthTrend >= 0 ? '↑' : '↓' }}
              {{ Math.abs(statistics.monthTrend) }}%
            </span>
            <span class="label">较上月</span>
          </div>
        </el-card>
      </el-col>

      <!-- 总访问量 -->
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="overview-card">
          <el-statistic title="总访问量" :value="statistics.totalViews">
            <template #prefix>
              <el-icon color="#F56C6C"><DataLine /></el-icon>
            </template>
          </el-statistic>
          <div class="trend">
            <span class="label">累计统计</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <!-- 添加 ECharts 折线图展示访问趋势 -->
    <el-card class="chart-card">
      <template #header>
        <div class="card-header">
          <span>访问趋势</span>
          <el-radio-group v-model="chartType" size="small" @change="handleChartTypeChange">
            <el-radio-button value="day">按天</el-radio-button>
            <el-radio-button value="week">按周</el-radio-button>
            <el-radio-button value="month">按月</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <div ref="chartContainer" class="chart-container"></div>
    </el-card>

    <!-- 热门文章排行 -->
    <el-card class="ranking-card">
      <template #header>
        <div class="card-header">
          <span>热门文章排行</span>
        </div>
      </template>
      <el-table :data="topArticles" style="width: 100%">
        <el-table-column type="index" label="排名" />
        <el-table-column prop="title" label="文章标题" />
        <el-table-column prop="category" label="分类" />
        <el-table-column prop="tags" label="标签">
          <template #default="{ row }">
            <el-tag
                v-for="(tag, idx) in row.tags"
                :key="idx"
            >{{ tag }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="views" label="浏览量" />
        <el-table-column prop="stars" label="点赞数" />
        <el-table-column prop="comments" label="评论数" />
        <el-table-column prop="published_time" label="创建时间" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import {
  View,
  TrendCharts,
  DataAnalysis,
  DataLine
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getHotApi, getTrafficStatistics, getChartDataApi } from "@/api/posts/index.js"
import * as echarts from 'echarts'

/* ========== 响应式数据 ========== */

// 图表类型
const chartType = ref('day')

// 图表实例
let chartInstance = null

// 图表容器引用
const chartContainer = ref(null)

// 统计数据
const statistics = reactive({
  todayViews: 0,
  todayTrend: 0,
  weekViews: 0,
  weekTrend: 0,
  monthViews: 0,
  monthTrend: 0,
  totalViews: 0
})

// 热门文章
const topArticles = ref([])

const chartData = reactive({
  day: {
    dates: [],
    values: []
  },
  week: {
    dates: [],
    values: []
  },
  month: {
    dates: [],
    values: []
  }
})

/* ========== 方法 ========== */

/**
 * 获取热门top文章
 */
const handleGetTopArticles = async () => {
  const response = await getHotApi()
  if (response.code === 200) {
    topArticles.value = response.data.list
  } else {
    ElMessage.error(response.msg)
  }
}

/**
 * 处理获取流量数据统计
 */
const handleGetTrafficStatistics = async () => {
  const response = await getTrafficStatistics()
  if (response.code === 200) {
    statistics.todayViews = response.data.totalViews
    statistics.todayTrend = response.data.todayTrend
    statistics.weekViews = response.data.weekViews
    statistics.weekTrend = response.data.weekTrend
    statistics.monthViews = response.data.monthViews
    statistics.monthTrend = response.data.monthTrend
    statistics.totalViews = response.data.totalViews

    // 获取图表数据
    await fetchChartData()
  } else {
    ElMessage.error(response.msg)
  }
}

/**
 * 获取图表数据（真实接口）
 */
const fetchChartData = async () => {
  try {
    const response = await getChartDataApi()

    if (response.code === 200) {
      const chartDataRes = response.data.data.chartData
      // 使用真实的后端数据
      chartData.day = chartDataRes.day
      chartData.week = chartDataRes.week
      chartData.month = chartDataRes.month
      // 更新图表
      await nextTick()
      updateChart()
    } else {
      // 如果后端返回失败，使用模拟数据
      console.warn('获取图表数据失败，使用模拟数据')
      ElMessage.error(response.msg)
      await nextTick()
      updateChart()
    }
  } catch (error) {
    // 如果接口调用出错，使用模拟数据
    console.error('图表数据接口调用出错:', error)
    ElMessage.warning('图表数据加载失败，使用模拟数据展示')
    await nextTick()
    updateChart()
  }
}

/**
 * 初始化 ECharts 图表
 */
const initChart = () => {
  if (!chartContainer.value) return

  // 初始化图表实例
  chartInstance = echarts.init(chartContainer.value)

  // 更新图表
  updateChart()

  // 监听窗口大小变化，自动调整图表尺寸
  window.addEventListener('resize', handleResize)
}

/**
 * 更新图表数据
 */
const updateChart = () => {
  if (!chartInstance) return

  const currentData = chartData[chartType.value]

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: currentData.dates,
      axisLine: {
        lineStyle: {
          color: 'var(--el-border-color)'
        }
      },
      axisLabel: {
        color: 'var(--el-text-color-regular)'
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: 'var(--el-border-color)'
        }
      },
      axisLabel: {
        color: 'var(--el-text-color-regular)'
      },
      splitLine: {
        lineStyle: {
          color: 'var(--el-border-color-lighter)'
        }
      }
    },
    series: [
      {
        name: '访问量',
        type: 'line',
        smooth: true,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              {
                offset: 0,
                color: 'rgba(64, 158, 255, 0.3)'
              },
              {
                offset: 1,
                color: 'rgba(64, 158, 255, 0.05)'
              }
            ]
          }
        },
        lineStyle: {
          color: '#409EFF',
          width: 2
        },
        itemStyle: {
          color: '#409EFF'
        },
        data: currentData.values
      }
    ]
  }

  chartInstance.setOption(option)
}

/**
 * 处理图表类型变化
 */
const handleChartTypeChange = () => {
  updateChart()
}

/**
 * 处理窗口大小变化
 */
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

/* ========== 生命周期 ========== */

onMounted(async () => {
  await handleGetTopArticles()
  await handleGetTrafficStatistics()

  await nextTick()
  initChart()
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
/* ========== 面板容器样式 ========== */
.statistics-panel {
  width: 100%;
}

/* ========== 面板标题样式 ========== */
.panel-header {
  margin-bottom: 24px;
}

.panel-header h2 {
  font-size: 28px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.panel-header p {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

/* ========== 概览卡片样式 ========== */
.overview-row {
  margin-bottom: 20px;
}

.overview-card {
  margin-bottom: 20px;
}

.trend {
  margin-top: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.trend .up {
  color: var(--el-color-success);
  font-weight: 600;
}

.trend .down {
  color: var(--el-color-danger);
  font-weight: 600;
}

.trend .label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

/* ========== 图表卡片样式 ========== */
.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

/* 图表容器样式 */
.chart-container {
  width: 100%;
  height: 400px;
}

/* ========== 排行卡片样式 ========== */
.ranking-card {
  margin-bottom: 20px;
}

/* ========== 移动端适配 ========== */
@media screen and (max-width: 768px) {
  .panel-header h2 {
    font-size: 24px;
  }

  /* 移动端图表高度调整 */
  .chart-container {
    height: 300px;
  }
}

@media screen and (max-width: 480px) {
  .panel-header h2 {
    font-size: 20px;
  }

  /* 小屏幕图表高度调整 */
  .chart-container {
    height: 250px;
  }

  /* 小屏幕卡片头部布局调整 */
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>
