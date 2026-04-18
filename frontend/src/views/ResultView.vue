<template>
  <div class="result-page">
    <el-container>
      <el-header class="page-header">
        <div class="header-content">
          <div class="logo">
            <el-icon :size="28" color="#409EFF"><Document /></el-icon>
            <span>简历解析结果</span>
          </div>
          <el-button @click="goBack" type="primary" plain>
            <el-icon><ArrowLeft /></el-icon>
            返回上传
          </el-button>
        </div>
      </el-header>

      <el-main class="page-main">
        <div v-if="resumeData" class="result-content">
          <!-- 岗位匹配卡片 -->
          <el-card class="match-card" shadow="hover">
            <template #header>
              <h3>
                <el-icon><Trophy /></el-icon>
                岗位匹配分析
              </h3>
            </template>

            <!-- 岗位描述输入 -->
            <div v-if="!matchResult" class="job-input-section">
              <el-input
                v-model="jobDescription"
                type="textarea"
                :rows="6"
                placeholder="请输入招聘岗位描述，AI将分析岗位需求并与简历进行匹配..."
                resize="none"
              />
              <el-button
                type="primary"
                class="analyze-btn"
                :loading="isAnalyzing"
                @click="analyzeMatch"
              >
                <el-icon><Search /></el-icon>
                开始匹配分析
              </el-button>
            </div>

            <!-- 匹配结果展示 -->
            <div v-else class="match-result">
              <!-- 总体评分 -->
              <div class="score-section">
                <div class="overall-score">
                  <el-progress
                    type="dashboard"
                    :percentage="parseInt(matchResult.overallScore)"
                    :color="scoreColors"
                    :stroke-width="12"
                  />
                  <div class="score-label">总体匹配度</div>
                </div>
                <div class="detail-scores">
                  <div class="score-item">
                    <span class="label">技能匹配</span>
                    <el-progress :percentage="parseInt(matchResult.skillScore)" :stroke-width="8" />
                  </div>
                  <div class="score-item">
                    <span class="label">经验匹配</span>
                    <el-progress :percentage="parseInt(matchResult.experienceScore)" :stroke-width="8" />
                  </div>
                  <div class="score-item">
                    <span class="label">学历匹配</span>
                    <el-progress :percentage="parseInt(matchResult.educationScore)" :stroke-width="8" />
                  </div>
                </div>
              </div>

              <el-divider />

              <!-- 岗位需求 -->
              <div class="job-requirements">
                <h4>岗位需求分析</h4>
                <p><strong>岗位名称：</strong>{{ jobRequirements?.position || '-' }}</p>
                <p><strong>最低工作年限：</strong>{{ jobRequirements?.minWorkYears || '-' }}</p>
                <p><strong>学历要求：</strong>{{ jobRequirements?.educationRequirement || '-' }}</p>
                <div v-if="jobRequirements?.requiredSkills?.length">
                  <strong>必需技能：</strong>
                  <el-tag v-for="skill in jobRequirements.requiredSkills" :key="skill" type="danger" class="skill-tag">
                    {{ skill }}
                  </el-tag>
                </div>
              </div>

              <el-divider />

              <!-- 技能匹配情况 -->
              <div class="skills-match">
                <h4>技能匹配情况</h4>
                <div v-if="matchResult.matchedSkills?.length" class="matched">
                  <p class="section-title">
                    <el-icon color="#67C23A"><CircleCheck /></el-icon>
                    已匹配技能 ({{ matchResult.matchedSkills.length }})
                  </p>
                  <el-tag v-for="skill in matchResult.matchedSkills" :key="skill" type="success" class="skill-tag">
                    {{ skill }}
                  </el-tag>
                </div>
                <div v-if="matchResult.missingSkills?.length" class="missing">
                  <p class="section-title">
                    <el-icon color="#F56C6C"><Warning /></el-icon>
                    缺失技能 ({{ matchResult.missingSkills.length }})
                  </p>
                  <el-tag v-for="skill in matchResult.missingSkills" :key="skill" type="info" class="skill-tag">
                    {{ skill }}
                  </el-tag>
                </div>
              </div>

              <el-divider />

              <!-- 分析说明 -->
              <div class="analysis">
                <h4>匹配分析</h4>
                <el-alert
                  :title="matchResult.analysis"
                  type="info"
                  :closable="false"
                  show-icon
                />
              </div>

              <el-button @click="resetMatch" class="reset-btn">重新匹配</el-button>
            </div>
          </el-card>

          <!-- 简历信息卡片 -->
          <el-card class="info-card" shadow="hover">
            <template #header>
              <h3>
                <el-icon><User /></el-icon>
                基本信息
              </h3>
            </template>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="姓名" :span="1">
                {{ resumeData.name || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="电话" :span="1">
                <el-icon><Phone /></el-icon>
                {{ resumeData.phone || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="邮箱" :span="2">
                <el-icon><Message /></el-icon>
                {{ resumeData.email || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="地址" :span="2">
                <el-icon><Location /></el-icon>
                {{ resumeData.address || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="求职意向" :span="2">
                {{ resumeData.intention || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="期望薪资" :span="1">
                {{ resumeData.salary || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="工作年限" :span="1">
                {{ resumeData.workYear || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="学历背景" :span="2">
                {{ resumeData.education || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="工作经历" :span="2">
                <pre style="white-space: pre-wrap; margin: 0;">{{ resumeData.workExperience || '-' }}</pre>
              </el-descriptions-item>
              <el-descriptions-item label="项目经历" :span="2">
                <pre style="white-space: pre-wrap; margin: 0;">{{ resumeData.project || '-' }}</pre>
              </el-descriptions-item>
              <el-descriptions-item label="技能" :span="2">
                {{ resumeData.skills || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="语言" :span="1">
                {{ resumeData.language || '-' }}
              </el-descriptions-item>
              <el-descriptions-item label="证书" :span="1">
                {{ resumeData.certificates || '-' }}
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </div>

        <el-empty v-else description="暂无数据，请先上传简历" />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Document,
  ArrowLeft,
  User,
  Phone,
  Message,
  Location,
  Trophy,
  Search,
  CircleCheck,
  Warning
} from '@element-plus/icons-vue'
import { matchResume } from '../api/resume'
import type { ResumeInfo, MatchResult, JobRequirements } from '../types'

const router = useRouter()

const resumeData = ref<ResumeInfo | null>(null)
const jobDescription = ref('')
const isAnalyzing = ref(false)
const matchResult = ref<MatchResult | null>(null)
const jobRequirements = ref<JobRequirements | null>(null)

const scoreColors = [
  { color: '#f56c6c', percentage: 60 },
  { color: '#e6a23c', percentage: 80 },
  { color: '#67c23a', percentage: 100 }
]

onMounted(() => {
  // 从 sessionStorage 获取数据
  const stored = sessionStorage.getItem('resumeData')
  if (stored) {
    try {
      resumeData.value = JSON.parse(stored)
    } catch (e) {
      ElMessage.error('数据解析失败')
    }
  } else {
    ElMessage.warning('未找到简历数据，请重新上传')
  }
})

const analyzeMatch = async () => {
  if (!jobDescription.value.trim()) {
    ElMessage.warning('请输入岗位描述')
    return
  }
  if (!resumeData.value) {
    ElMessage.error('简历数据不存在')
    return
  }

  isAnalyzing.value = true
  try {
    const result = await matchResume(resumeData.value, jobDescription.value)
    if (result.code === 200 && result.data) {
      matchResult.value = result.data.matchResult
      jobRequirements.value = result.data.jobRequirements
      ElMessage.success('匹配分析完成！')
    } else {
      ElMessage.error(result.message || '匹配失败')
    }
  } catch (error) {
    ElMessage.error('匹配分析失败，请重试')
  } finally {
    isAnalyzing.value = false
  }
}

const resetMatch = () => {
  matchResult.value = null
  jobRequirements.value = null
  jobDescription.value = ''
}

const goBack = () => {
  router.push('/')
}
</script>

<style scoped lang="scss">
.result-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.page-header {
  background: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 0;

  .header-content {
    max-width: 1200px;
    margin: 0 auto;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;

    .logo {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 20px;
      font-weight: 600;
      color: #303133;
    }
  }
}

.page-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px;
}

.result-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  max-width: 1400px;
  margin: 0 auto;

  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
}

.match-card {
  height: fit-content;

  h3 {
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    color: #303133;
  }

  .job-input-section {
    .analyze-btn {
      width: 100%;
      margin-top: 16px;
      height: 44px;
    }
  }

  .match-result {
    .score-section {
      display: flex;
      gap: 40px;
      align-items: center;
      margin-bottom: 20px;

      .overall-score {
        text-align: center;

        .score-label {
          margin-top: 10px;
          font-size: 16px;
          color: #303133;
          font-weight: 500;
        }
      }

      .detail-scores {
        flex: 1;

        .score-item {
          margin-bottom: 16px;

          .label {
            display: block;
            margin-bottom: 6px;
            font-size: 14px;
            color: #606266;
          }
        }
      }
    }

    h4 {
      margin: 16px 0 12px;
      font-size: 15px;
      color: #303133;
    }

    .job-requirements {
      p {
        margin: 8px 0;
        color: #606266;
      }
    }

    .skills-match {
      .section-title {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 14px;
        color: #606266;
        margin-bottom: 10px;
      }

      .matched, .missing {
        margin-bottom: 16px;
      }
    }

    .skill-tag {
      margin: 4px;
    }

    .reset-btn {
      margin-top: 20px;
      width: 100%;
    }
  }
}

.info-card {
  h3 {
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    color: #303133;
  }

}

@media (max-width: 768px) {
  .page-main {
    padding: 16px;
  }

  .result-content {
    gap: 16px;
  }
}
</style>
