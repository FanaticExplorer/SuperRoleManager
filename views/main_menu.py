import discord
from views.category_menu import CategoryMenuView


class MainMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # noinspection PyUnusedLocal
    @discord.ui.button(
        label="Приступим!",
        emoji=discord.PartialEmoji.from_str("<:FP_whitewolf_Mmmmm:1445417863060918424>"),
        style=discord.ButtonStyle.primary,
        custom_id="persistent_main_menu_button",
    )
    async def open_menu(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ):
        await interaction.response.defer(ephemeral=True)

        view = CategoryMenuView(guild=interaction.guild)
        embed = discord.Embed(
            title="Выберите требуемую для вас категорию. <:FP_firzp:1530656627823476786>",
            description="Мы готовы записывать ваши желания и выдавать вам роли.",
            color=0xefa05d
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1018534366797889536/1487468285892235504/2embed.png?ex=69c9404b&is=69c7eecb&hm=14665c5e652b3c4be85168078119dc9b8e3d3deec72ca9b1b4798ee4892021a1&")
        embed.set_footer(text="Все роли выбранные вами подсвечиваются зеленым и при повторном нажатии на них они будут убраны.")

        await interaction.followup.send(embed=embed, ephemeral=True, view=view)
