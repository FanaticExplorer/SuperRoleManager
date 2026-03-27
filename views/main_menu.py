import discord
from views.category_menu import CategoryMenuView

class MainMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Выбрать роли", style=discord.ButtonStyle.primary, custom_id="persistent_main_menu_button")
    async def open_menu(self, button: discord.ui.Button, interaction: discord.Interaction):
        view = CategoryMenuView()
        embed = discord.Embed(title="Выберите категорию", color=0x3498db)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
