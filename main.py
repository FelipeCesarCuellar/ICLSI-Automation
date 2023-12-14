import DataExtractionModule
import ThresholdTensionModule

dataframes = DataExtractionModule.execute()

print(f"[INFO] Foram carregados {len(dataframes)} dataframe(s)")

#################################
# Chamada de módulos de cálculo #
#################################

#################################
# Chamada de módulo de export   #
#################################

ThresholdTensionModule.execute(dataframes)
