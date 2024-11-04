# A comparison of popular stock performance ratios to gross profit margin and overall stock success



install.packages("tidyverse")
library(tidyverse)



income_wrangled <- us_income_annual |> 
  select(-`Fiscal Period`, -`Report Date`, -`Publish Date`, -`Restated Date`, -Currency)


balance_wrangled<-us_balance_annual |> 
  select(-`Fiscal Period`, -`Report Date`, -`Publish Date`, -`Restated Date`, -Currency)

balance_wrangled<-balance_wrangled |> 
  mutate(current_ratio = `Total Current Assets`/`Total Current Liabilities`) |> 
  mutate(current_group = case_when(current_ratio>=2.0 ~ "Great", 
                                   current_ratio>=1.2 & current_ratio<2.0 ~ "Good", 
                                   current_ratio>=1.0 & current_ratio <1.2 ~ "Ok" , 
                                   TRUE ~ "Bad")) 
  #mutate(quick_ratio = `Total Current Assets` - Inventories - ) 
  
us_merge <- merge(balance_wrangled, income_wrangled) #inner joining tables

#debt ratio
us_merge<-us_merge |> 
  mutate(debt_ratio = (`Long Term Debt`+`Short Term Debt`)/`Total Liabilities & Equity`)


#PE ratio, net income / shares (diluted)- treasury stock
us_merge<-us_merge |> 
  mutate(PE_ratio = `Net Income`/(`Shares (Diluted)`- `Treasury Stock`))

#AVG shareholder equity 
us_merge<-us_merge |> 
  group_by(Ticker) |> 
  mutate(avg_shareholder_equity = (`Total Assets`- `Total Liabilities`))

#Return on Equity
us_merge<-us_merge |> 
  mutate(ROE = `Net Income`/avg_shareholder_equity)

#debt to equity ratio
us_merge<-us_merge |> 
  mutate(equity_ratio = (`Total Assets`- `Total Liabilities`)/`Total Assets`)
us_merge<-us_merge |> 
  rename(debt_to_equity_ratio = equity_ratio)

#return on assets ratio
us_merge<-us_merge |> 
  group_by(Ticker) |> 
  mutate(avg_total_assets = mean(`Total Assets`))
us_merge<-us_merge |> 
  mutate(Return_on_Assets = `Net Income`/avg_total_assets)

# ---GRAPHS---

#more clean up before graphs
us_merge<-us_merge |> 
  select(-`Shares (Basic)`, -`Depreciation & Amortization`, -`Abnormal Gains (Losses)`, -`Net Extraordinary Gains (Losses)`)

#Gross Profit Margin, measure of success
us_merge<-us_merge |> 
  mutate(Gross_profit_margin = (Revenue - `Cost of Revenue`)/Revenue)

#making current group a factor variable 
levels(us_merge$current_group)
us_merge<-us_merge |> 
  mutate(current_group = as.factor(current_group))


us_merge<-us_merge |> 
  group_by(current_group, `Fiscal Year`) |> 
  mutate(avg_gross_profitmargin_by_year = mean(Gross_profit_margin, na.rm = TRUE)) 

#Graph of current ratio/group
us_merge |> 
  ggplot(aes(x = `Fiscal Year`, y = avg_gross_profitmargin_by_year, color = current_group)) +
  geom_line()+
  labs(title = "Does the Current Ratio actually Help?", x = "Year",y = "Average Gross Profit Margin" )


levels(us_merge$current_group)

# --- Current Ratio graphs ---


#Does a Great current ratio matter?
  
  avg_y_current = mean(subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 600 & current_group == "Great")$Gross_profit_margin)
  avg_x_current =  mean(subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 600 & current_group == "Great")$current_ratio)
  #x is ratio, y is profit margin
  
  ggplot(us_merge,aes(x = current_ratio, y = Gross_profit_margin, color = current_group)) +
  geom_point(data = subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 600 & current_group == "Great"), color = "blue") +
  labs(x = "Current Ratio", y = "Gross Profit Margin", title = "Does a Great current ratio matter?", fill = "Current Group") +
  geom_point(aes(x = avg_x_current
                 , y = avg_y_current), color = "black", size = 3) +
  annotate("text", x = avg_x_current, y = avg_y_current, label = paste("(", round(avg_x_current, 2), ",", round(avg_y_current, 2), ")"),
           vjust = -1, hjust = -0.5, color = "black")

#How does a Good ratio compare
  
  avg_y_current = mean(subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 150 & current_group == "Good")$Gross_profit_margin)
  avg_x_current =  mean(subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 150 & current_group == "Good")$current_ratio)
  #x is ratio, y is profit margin
  
  ggplot(us_merge,aes(x = current_ratio, y = Gross_profit_margin, color = current_group)) +
    geom_point(data = subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 150 & current_group == "Good"),color = "green") +
    labs(x = "Current Ratio", y = "Gross Profit Margin", title = "Good Current Ratio", fill = "Current Group") +
    geom_point(aes(x = avg_x_current
                   , y = avg_y_current), color = "black", size = 3) +
    annotate("text", x = avg_x_current, y = avg_y_current, label = paste("(", round(avg_x_current, 2), ",", round(avg_y_current, 2), ")"),
             vjust = -2, hjust = 0.5, color = "black")

#Ok current ratio 
  avg_y_current = mean(subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 600 & current_group == "Ok")$Gross_profit_margin)
  avg_x_current =  mean(subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 600 & current_group == "Ok")$current_ratio)
  #x is ratio, y is profit margin
  
  ggplot(us_merge,aes(x = current_ratio, y = Gross_profit_margin, color = current_group)) +
    geom_point(data = subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 600 & current_group == "Ok"), color = "lightblue") +
    labs(x = "Current Ratio", y = "Gross Profit Margin", title = "Ok Current Ratio", fill = "Current Group") +
    geom_point(aes(x = avg_x_current
                   , y = avg_y_current), color = "black", size = 3) +
    annotate("text", x = avg_x_current, y = avg_y_current, label = paste("(", round(avg_x_current, 2), ",", round(avg_y_current, 2), ")"),
             vjust = 1, hjust = -0.1, color = "black")
#Bad current ratio
  avg_y_current = mean(subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 600 & current_group == "Bad")$Gross_profit_margin)
  avg_x_current =  mean(subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 600 & current_group == "Bad")$current_ratio)
  #x is ratio, y is profit margin
  
  ggplot(us_merge,aes(x = current_ratio, y = Gross_profit_margin, color = current_group)) +
    geom_point(data = subset(us_merge, Gross_profit_margin >= 0 & current_ratio <= 600 & current_group == "Bad"),color = "violet") +
    labs(x = "Current Ratio", y = "Gross Profit Margin", title = "Bad Current Ratio", fill = "Current Group") +
    geom_point(aes(x = avg_x_current
                   , y = avg_y_current), color = "black", size = 3) +
    annotate("text", x = avg_x_current, y = avg_y_current, label = paste("(", round(avg_x_current, 2), ",", round(avg_y_current, 2), ")"),
             vjust = -2.3, hjust = 0.2, color = "black")

# --- PE ratio ---
  
  us_merge |> 
    filter(PE_ratio >= -200) |> 
    ggplot(aes(x= PE_ratio, y= Gross_profit_margin, color = `Fiscal Year`)) +
    geom_point()
  us_merge |> 
    filter(PE_ratio >=-20 & PE_ratio <=20) |> 
    ggplot(aes(x= PE_ratio, y= Gross_profit_margin, color = `Fiscal Year`)) +
    geom_point()

  # --- Debt to Equity ratio --- 
  
us_merge |> 
  filter(Gross_profit_margin>=-50) |>
  filter(debt_to_equity_ratio>=-100) |> 
  ggplot(aes(x=debt_to_equity_ratio, y= Gross_profit_margin, color = `Fiscal Year`))+
  geom_point()



