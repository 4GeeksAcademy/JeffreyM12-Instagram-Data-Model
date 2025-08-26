from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Post(db.Model):
    __tablename__ = "Post"
    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(200), nullable=False)
    caption: Mapped[str] = mapped_column(String(400))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    
    user: Mapped["Like"] = relationship(back_populates="liked_post")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")

class Comment(db.Model):
    __tablename__ = "Comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("Post.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

class Like(db.Model):
    __tablename__ = "Like"
    id: Mapped[int] = mapped_column(primary_key=True)
    liked_post: Mapped[int] = mapped_column(Integer, ForeignKey("Post.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes")