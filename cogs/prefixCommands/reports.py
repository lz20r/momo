import discord
from discord.ext import commands
from discord.ui import Select, View, Button

class ReportView(View):
    def __init__(self):
        super().__init__()

        self.add_item(
            Select(
                placeholder="Selecciona un informe",
                options=[
                    discord.SelectOption(label="Informe 1", value="report_1"),
                    discord.SelectOption(label="Informe 2", value="report_2"),
                    discord.SelectOption(label="Informe 3", value="report_3"),
                ],
            )
        )

        self.add_item(
            Button(
                style=discord.ButtonStyle.primary,
                label="Enviar",
                custom_id="send_report",
            )
        )

    async def interaction_check(self, interaction):
        # Solo permitir interacciones del autor original
        return interaction.user == self.message.author

class ReportsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reportes", aliases=["reps"])
    async def reports(self, ctx):
        view = ReportView()
        await ctx.send("Selecciona un informe:", view=view)

    @commands.Cog.listener() 
    async def on_select_option(self, interaction):
        if interaction.custom_id == "send_report":
            selected_option = interaction.values[0]
            await interaction.response.send_message(f"Has seleccionado: {selected_option}")

async def setup(bot):
    await bot.add_cog(ReportView(bot))    