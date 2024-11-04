library(tidyverse)
install.packages("gt")
library(gt)

#looking specifically at stock data, much simpler data

stock_data <- Exercise_9_stock_data_performance_fundamentals



stock_data |> 
  filter(`RoE`>=0 & `RoE`<=0.4) |> 
  ggplot(aes(x= `RoE`, y=Perf))+
  geom_point()+
  geom_smooth(method = "lm", se = FALSE, color = "Red")+
  labs(x="Return on Equity(RoE)", y = "Stock Performance", 
       title = "Does RoE have a Correlation with Stock Peformance?")

library(ggplot2)


#Return on Equity graph 
stock_data %>%
  filter(RoE >= 0 & RoE <= 0.4) %>%
  ggplot(aes(x = RoE, y = Perf)) +
  geom_point(color = "steelblue", alpha = 0.6, size = 3) +  # Adjust point aesthetics
  geom_smooth(method = "lm", se = FALSE, color = "red", linetype = "dashed", size = 1) +  # Adjust smooth line aesthetics
  labs(
    x = "Return on Equity (RoE)",
    y = "Stock Performance",
    title = "Correlation between RoE and Stock Performance"
  ) +
  theme_minimal() +  # Set a minimal theme
  theme(
    plot.title = element_text(size = 16, face = "bold"),
    axis.title = element_text(size = 14),
    axis.text = element_text(size = 12),
    legend.position = "none"  # Remove legend
  )


stock_data<-stock_data |> 
  mutate(perf_group = case_when(Perf>=0.4 ~ "Great", 
                                   Perf>=0 & Perf<0.4 ~ "Good", 
                                   TRUE ~ "Bad")) 

stock_data<-stock_data |> 
  mutate(perf_group = as.factor(perf_group)) |> 
  fct_reorder(perf_group,.desc = TRUE)

levels(stock_data$perf_group)



stock_data |> 
  filter(`Debt/Equity`<=25 & `P/E`<=100) |> 
  ggplot(aes(x=`Debt/Equity`,y=`P/E`, color = perf_group))+
  geom_point()+
  labs(title = "Is there a Trend between P/E + D/E that relates to Stock Performance?")+
  geom_smooth(method = "lm",se = FALSE)

cor(stock_data$RoE,stock_data$Perf)

names(stock_data)

stock_data <-stock_data |> 
  rename("ID" = ...1)

PE_perf <- stock_data |> 
  select(ID,`P/E`, Perf) |> 
  arrange(desc(`P/E`)) |> 
  head()

PE_perf %>%
  gt() %>%
  tab_header(
    title = "Top Stocks by P/E Ratio",
    subtitle = "Showing the top 6 stocks by P/E ratio and their performance"
  ) %>%
  fmt_number(
    columns = vars(`P/E`, Perf),
    decimals = 2
  ) %>%
  fmt_number(
    columns = vars(Perf),
    suffixing = TRUE
  ) %>%
  tab_style(
    style = list(
      cell_fill(color = "lightblue"),
      cell_text(weight = "bold")
    ),
    locations = cells_body()
  ) %>%
  tab_spanner(
    label = "Performance",
    columns = vars(Perf)
  ) %>%
  tab_spanner(
    label = "P/E Ratio",
    columns = vars(`P/E`)
  )
stock_data |> 
  filter(`P/E`>=-50 & `P/E`<=100) |> 
  ggplot(aes(x=`P/E`,y=Perf))+
  geom_point()+
  geom_smooth(method="lm", se = FALSE)

cor(stock_data$Perf,stock_data$`P/E`)    

stock_data |> 
  #filter(`P/B`<=50) |> 
  ggplot(aes(x=`Working Capital Ratio`,y=Perf))+
  geom_point()+
  geom_smooth(method="lm", se = FALSE)
stock_data |> 
  ggplot(aes(x=`Working Capital Ratio`,y=`P/E`, color = Perf))+
  geom_point()
  #geom_smooth(method="lm", se = FALSE)


