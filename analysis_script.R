#Set working directory
setwd("C:/Users/harry/iCloudDrive/Masters of IT/2019 - Semester 1/IFN702 - Project 2/SQL")

#import required libraries
library(dplyr)
library(tidyverse)
library(forcats)
library(broom)
library(goftest)
library(ggplot2)
library(GGally)

survey_df <- read_csv("702_data_extraction.csv")


#convert variable classes to appropriate class types
sapply(survey_df, class)
summary(survey_df)
survey_df$Technician <- factor(survey_df$Technician)
survey_df$TechnicianTeam <- factor(survey_df$TechnicianTeam)
survey_df$SurveyTaker <- factor(survey_df$SurveyTaker)
survey_df$Score <- as.numeric(survey_df$Score)
survey_df$Service <- factor(survey_df$Service)
survey_df$Category <- factor(survey_df$Category)
survey_df$Subcategory <- factor(survey_df$Subcategory)
survey_df$Priority <- as.numeric(survey_df$Priority)
survey_df$Source <- factor(survey_df$Source) 
survey_df$CreatedDateTime <- as.Date(survey_df$CreatedDateTime , "%d/%m/%Y") #
survey_df$Stat_DateTimeResolved <- as.Date(survey_df$Stat_DateTimeResolved, "%d/%m/%Y") #
survey_df$Stat_SLAResponseBreached <- factor(survey_df$Stat_SLAResponseBreached) 
survey_df$Stat_SLAResolutionBreached <- factor(survey_df$Stat_SLAResolutionBreached)
sapply(survey_df, class)

#Filter out non IT teams
survey_df <- filter(survey_df, TechnicianTeam != "BTP")
survey_df <- filter(survey_df, TechnicianTeam != "Cherwell Admin")
survey_df <- filter(survey_df, TechnicianTeam != "Core Systems")
survey_df <- filter(survey_df, TechnicianTeam != "CRM Support")
survey_df <- filter(survey_df, TechnicianTeam != "DBSi")
survey_df <- filter(survey_df, TechnicianTeam != "HD Technology MineStar Team")
survey_df <- filter(survey_df, TechnicianTeam != "HD Technology Service Desk")
survey_df <- filter(survey_df, TechnicianTeam != "HR Services")
survey_df <- filter(survey_df, TechnicianTeam != "IT Manager")
survey_df <- filter(survey_df, TechnicianTeam != "IT Service & Support Manager")
survey_df <- filter(survey_df, TechnicianTeam != "Payroll")
survey_df <- filter(survey_df, TechnicianTeam != "Solutions Integration")
survey_df <- filter(survey_df, TechnicianTeam != "WMS Ops Support")
survey_df <- filter(survey_df, TechnicianTeam != "XAPT")
survey_df <- filter(survey_df, TechnicianTeam != "dbsi")

#Score histogram
ggplot(data = survey_df, aes(x = Score)) +
  geom_histogram(bins = 20, color = "black", fill = "grey") +
  labs(x = "Average Score", y = "Count") + 
  facet_wrap( ~ TechnicianTeam) +
  theme_bw()

survey_df %>%
  ggplot(aes(y =Score)) +
  geom_boxplot(colour = "black", fill = "grey") +
  scale_y_continuous(limits = c(0,5)) +
  theme_bw() +
  facet_wrap( ~ TechnicianTeam) +
  labs(y = "Survey Score", x = "Service")

survey_df %>%
  mutate(TechnicianTeam = fct_lump(TechnicianTeam, n=-5)) %>%
  ggplot(aes(y =Score, x = TechnicianTeam)) +
  geom_boxplot(colour = "black", fill = "grey") +
  scale_y_continuous(limits = c(0,5)) +
  theme_bw() +
  labs(y = "Survey Score", x = "Service")

survey_df %>%
  ggplot(aes(y =Score, x = Service)) +
  geom_point(colour = "black", fill = "grey") +
  scale_y_continuous(limits = c(0,5)) +
  theme_bw() +
  facet_wrap( ~ TechnicianTeam) +
  labs(y = "Survey Score", x = "Service")

summary(survey_df)
